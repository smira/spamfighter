<?php
/*
Plugin Name: Spam Fighter for comments
Description: Плагин проверяет комменты через API СпамоБорца. Сообщения помечает в соответствии с настройками Wordpress: для каждого статуса сообщения заданы ответы сервера СпамоБорца. Учитывается статус комментария, который определил Wordpress.
Version: 1.0
Author: Grishina Julia
*/

require_once('json/SF_API_JSON.php');

$sf_textdomain = 'spamfighter';

add_option('sf_api_url', 'http://localhost:8000/api/json/');

add_option('sf_approved_words', 'OK');

add_option('sf_pending_words', 'FREQUENT');

add_option('sf_spam_words', 'INVALID, SPAM');

load_plugin_textdomain($sf_textdomain, 'wp-content/plugins/spamfighter');

function sf_settings_page ()
{
    global $sf_textdomain;

    if (function_exists('add_options_page')) {
        add_options_page( __('SpamFighter Settings', $sf_textdomain), __('SFSettings', $sf_textdomain), 8, basename(__FILE__), 'sf_settings_form' );
    }
}

function sf_settings_form()
{
    global $sf_textdomain;

    $api_url = get_option('sf_api_url');
    $approved_words = get_option('sf_approved_words');
    $pending_words = get_option('sf_pending_words');
    $spam_words = get_option('sf_spam_words');
    
    if ( isset($_POST['submit']) ) {   
        if ( function_exists('current_user_can') && !current_user_can('manage_options') )
            wp_die ( __('Invalid user', $sf_textdomain) );
        
        if (function_exists ('check_admin_referer') )
            check_admin_referer('sf_form');
        
        $api_url = $_POST['sf_api_url'];
        $approved_words = $_POST['sf_approved_words'];
        $pending_words = $_POST['sf_pending_words'];
        $spam_words = $_POST['sf_spam_words'];
        
        update_option('sf_api_url', $api_url);
        update_option('sf_approved_words', $approved_words);
        update_option('sf_pending_words', $pending_words);
        update_option('sf_spam_words', $spam_words);
    }
    ?>
    <div class='wrap'>
        <h2><?php _e("SpamFighter Settings", $sf_textdomain); ?></h2>
        
        <form name="sf" method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>?page=spamfighter.php&amp;updated=true">

            <?php 
                if (function_exists ('wp_nonce_field') )
                    wp_nonce_field('sf_form'); 
            ?>
            
            <table class="form-table">
                <tr valign="top">
                    <th scope="row"><?php _e("API URL:", $sf_textdomain); ?></th>                    
                    <td>
                        <input type="text" name="sf_api_url" size="80" value="<?php echo $api_url; ?>" />
                    </td>
                </tr>
                
                <tr valign="top">
                    <th scope="row"><?php _e("Mark message as approved for server response:", $sf_textdomain); ?></th>
                    <td>
                        <input type="text" name="sf_approved_words" size="80" value="<?php echo $approved_words; ?>" />
                    </td>
                </tr>
                
                <tr valign="top">
                    <th scope="row"><?php _e("Mark message as pending for server response:", $sf_textdomain); ?></th>
                    <td>
                        <input type="text" name="sf_pending_words" size="80" value="<?php echo $pending_words; ?>" />
                    </td>
                </tr>
                
                <tr valign="top">
                    <th scope="row"><?php _e("Mark message as spam for server response:", $sf_textdomain); ?></th>
                    <td>
                        <input type="text" name="sf_spam_words" size="80" value="<?php echo $spam_words; ?>" />
                    </td>
                </tr>                

            </table>

            <input type="hidden" name="action" value="update" />
            <input type="hidden" name="page_options" value="api_url,sf_approved_words,sf_pending_words,sf_spam_words" />

            <p class="submit">
            <input type="submit" name="submit" value="Save Changes" />
            </p>
        </form>
    </div>
<?php
}

function sf_preprocess_comment($commentdata)
{
    global $wpdb;
    
    $comment = $commentdata['comment_content'];
    $user_id = $commentdata['user_ID'];
    $comment_post_ID = $commentdata['comment_post_ID'];
    
    $api_url = get_option('sf_api_url');
    $approved_words = get_option('sf_approved_words');
    $pending_words = get_option('sf_pending_words');
    $spam_words = get_option('sf_spam_words');
    
    $approved_words_list = preg_split("/[\s,]+/", $approved_words);
    $pending_words_list = preg_split("/[\s,]+/", $pending_words);
    $spam_words_list = preg_split("/[\s,]+/", $spam_words);
    
    if ( $user_id ) {
        $userdata = get_userdata($user_id);
        $user = new WP_User($user_id);
        $post_author = $wpdb->get_var($wpdb->prepare("SELECT post_author FROM $wpdb->posts WHERE ID = %d LIMIT 1", $comment_post_ID));
    }

    if ( isset($userdata) && ( $user_id == $post_author || $user->has_cap('moderate_comments') ) )
        return $commentdata;
    
    $api = new SF_API_JSON($api_url);
    $analyze = $api->messageInput(new SF_Message($comment, $user_id));
    
    $return = 0;
    if ($analyze == 'UNKNOWN' || in_array($analyze, $approved_words_list))
        $return = 1;
    elseif (in_array($analyze, $pending_words_list))
        $return = 0;
    elseif (in_array($analyze, $spam_words_list))
        $return = 'spam';

    add_filter('pre_comment_approved', create_function('$approved', 'return sf_comment_approved($approved, "' . $return . '");'));

    return $commentdata;
}

function sf_comment_approved($approved, $sf_approved)
{
    if ($approved === 'spam')
        $return = 'spam';
    elseif ($approved === 0) {
        if ($sf_approved === 0 || $sf_approved === 'spam')
            $return = $sf_approved;
        else
            $return = $approved;
    }
    else
        $return = $sf_approved;
        
    if ($return === 'spam')
        add_action('comment_post', 'sf_die');
    
    return $return;
}

function sf_die($comment_ID)
{
    global $sf_textdomain;

    wp_die( __('Your comment is spam!', $sf_textdomain) );
}
 
add_action('admin_menu', 'sf_settings_page');

add_action('preprocess_comment', 'sf_preprocess_comment');
?>