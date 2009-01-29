# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008, 2009 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# This file is part of SpamFighter.
#
# SpamFighter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpamFighter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SpamFighter.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Тесты на L{spamfighter.core.model}.
"""

class Texts:
    """
    Набор текстов для тестирования модели.
    """

    pushkin = u'''
Зачем я ею очарован?
Зачем расстаться должен с ней?
Когда б я не был избалован
Цыганской жизнию моей.
             __________

    Она глядит на вас так нежно,
Она лепечет так небрежно,
Она так тонко весела,
Ее глаза так полны чувством,
Вечор она с таким искусством
Из-под накрытого стола
Мне свою ножку подала.

Не спрашивай, зачем унылой думой
Среди забав я часто омрачен,
Зачем на все подъемлю взор угрюмый,
Зачем не мил мне сладкой жизни сон;

Не спрашивай, зачем душой остылой
Я разлюбил веселую любовь
И никого не называю милой —
Кто раз любил, уж не полюбит вновь;

Кто счастье знал, уж не узнает счастья.
На краткий миг блаженство нам дано:
От юности, от нег и сладострастья
Останется уныние одно...


Я верю: я любим; для сердца нужно верить.
Нет, милая моя не может лицемерить;
Все непритворно в ней: желаний томный жар,
Стыдливость робкая, харит бесценный дар,
Нарядов и речей приятная небрежность
И ласковых имен младенческая нежность.

В тревоге пестрой и бесплодной
Большого света и двора
Я сохранила взгляд холодный,
Простое сердце, ум свободный
И правды пламень благородный
И как дитя была добра;
Смеялась над толпою вздорной,
Судила здраво и светло,
И шутки злости самой черной
Писала прямо набело.
'''

    pushkin2 = u'''
    Она глядит на вас так нежно,
Она лепечет так небрежно,
Она так тонко весела,
Ее глаза так полны чувством,
Вечор она с таким искусством
Из-под накрытого стола
Мне свою ножку подала.

Не спрашивай, зачем унылой думой
Среди забав я часто омрачен,
Зачем на все подъемлю взор угрюмый,
Зачем не мил мне сладкой жизни сон;

Не спрашивай, зачем душой остылой
Я разлюбил веселую любовь
И никого не называю милой —
Кто раз любил, уж не полюбит вновь;

Кто счастье знал, уж не узнает счастья.
На краткий миг блаженство нам дано:
От юности, от нег и сладострастья
Останется уныние одно...


Я верю: я любим; для сердца нужно верить.
Нет, милая моя не может лицемерить;
Все непритворно в ней: желаний томный жар,
Стыдливость робкая, харит бесценный дар,
Нарядов и речей приятная небрежность
И ласковых имен младенческая нежность.

В тревоге пестрой и бесплодной
Большого света и двора
Я сохранила взгляд холодный,
Простое сердце, ум свободный
И правды пламень благородный
И как дитя была добра;
Смеялась над толпою вздорной,
Судила здраво и светло,
И шутки злости самой черной
Писала прямо набело.
    В последний раз твой образ милый
Дерзаю мысленно ласкать,
Будить мечту сердечной силой
И с негой робкой и унылой
Твою любовь воспоминать.

Бегут меняясь наши лета,
Меняя всё, меняя нас,
Уж ты для своего поэта
Могильным сумраком одета,
И для тебя твой друг угас.

Прими же, дальная подруга,
Прощанье сердца моего,
Как овдовевшая супруга,
Как друг, обнявший молча друга
Пред заточением его.

Я думал, что любовь погасла навсегда,
Что в сердце злых страстей умолкнул глас мятежный,
Что дружбы наконец отрадная звезда
Страдальца довела до пристани надежной.
Я мнил покоиться близ верных берегов,
Уж издали смотреть, указывать рукою
На парус бедственный пловцов,
Носимых яростной грозою.
И я сказал: «Стократ блажен,
Чей век, свободный и прекрасный,
Как век весны промчался ясной
И страстью не был омрачен,
Кто не страдал в любви напрасной,
Кому неведом грустный плен.
Блажен! но я блаженней боле.
Я цепь мученья разорвал,
Опять я дружбе... я на воле —
И жизни сумрачное поле
Веселый блеск очаровал!»
Но что я говорил... несчастный!
Минуту я заснул в неверной тишине,
Но мрачная любовь таилася во мне,
Не угасал мой пламень страстный.
Весельем позванный в толпу друзей моих,
Хотел на прежний лад настроить резву лиру,
Хотел еще воспеть прелестниц молодых,
Веселье, Вакха и Дельфиру.
Напрасно!.. я молчал; усталая рука
Лежала, томная, на лире непослушной,
Я все еще горел — и в грусти равнодушной
На игры младости взирал издалека.
Любовь, отрава наших дней,
Беги с толпой обманчивых мечтаний.
Не сожигай души моей,
Огонь мучительных желаний.
Летите, призраки... Амур, уж я не твой,
Отдай мне радости, отдай мне мой покой...
Брось одного меня в бесчувственной природе
Иль дай еще летать надежды на крылах,
Позволь еще заснуть и в тягостных цепях
Мечтать о сладостной свободе.
    '''

    udaff = u'''
        Вроде какие-то выборы скоро.
Мне однохуйственно как-то. Но всё ж
Взяли настырной рекламой за горло,
Мол, голосуй, а не то отсосёшь!
Я – гражданин, моя хата не с краю,
Надо, так надо! Об чем разговор!
Все приготовились?
Я выбираю:
Домик у моря, высокий забор,
Яхту под парусом, ясное небо,
Сауну, баню, джакузи, бассейн,
Спальни с каминами. Зрелищ и хлеба
Мир и покой для планеты для всей.
Я выбираю гараж, три машины,
Сад, где резвится детишек толпа.
Ну, и республик союз нерушимый,
Только без молота и без серпа.
Я выбираю раскованных женщин,
Тех, что всегда и поймут, и простят,
С грудью четвертым размером, не меньше,
И – с кругозором во всех областях.
Секс выбираю я лишь разнополый,
Всех содомитов сослать в Амстердам;
Новую сборную нам по футболу,
Если уж старая едет туда…
Но почему-то тех пунктов для выбора
Нет в избирательном списке моём:
Только фамилии – явные пидары,
Сволочи все, тунеядцы, ворьё.
Есть и на это идея вторая;
Если имеете вы интерес;
В утро воскресное
Я выбираю:
Сон до упора и утренний секс,
Там, где проснулись, и, может быть, дома,
Сразу с обеими или с одной,
Старой подругой, случайной знакомой
Или, на крайний же случай, с женой, …
Душ или ванна, а после процесса -
Сладкий горячий с баранками чай,
Тур к магазину, прогулка по лесу,
Или же в гости зайти невзначай.
День выбираю я неторопливый,
Небо и солнце в умытом окне,
Кружку литровую темного пива,
Блюдо креветок с лимончиком к ней,
День посвятить можно поиску клитора,
Поиску смысла и просто - хуйне.
В-общем, всегда есть свобода для выбора,
Чтоб не раскаяться в выборах мне.

Я видел фото в глянцевом журнале -
Не описать словами и пером:
Там негры пятиклассницу ебали.
Насильно. Без гандона. Впятером.

Вы скажете: "Ну да, и что такого?
Обычная для Гарлема хуйня".
Но фото было сделано в Коньково,
В метро - и тем расстроило меня.

Встаёт перед глазами непрестанно,
Как на перроне, с криком "Руки прочь!",
Безногий ветеран Афганистана
Рыдал в углу, не в силах ей помочь.

И, глядя, как бесчинствуют арапы,
Алкаш какой-то (ну не охуел?!)
Всю мелочь из его афганской шляпы
Сгребал себе в карман на опохмел...

Потом ещё пять фото в том же духе,
А хули вам - читатель любит жесть...
Неужто, кроме ёбаной чернухи
Нет ничего в журналах? Врёте - есть!

Мне мысль о том, что всё не так паршиво
Пришла, с жестокой правдой примирив:
Пусть этот снимок полон негатива.
Но сам он - несомненный позитив!


ЗЫ: Доктору Верховцеву спасибо за идею

Я грузинский солдат Амурадзе,
Я родился вблизи Телави,
Никогда я не слыл камикаде
На дорогаx грузинскиx в пыли.

Рос чернявым кудрявым повесой,
Пил вино, не курил анаши,
С Сулико, моей верной невестой,
Я любил миловаться в тиши.

Её губы краснее рубина
Смаковали в тени алычи,
Мое грубое тело грузина,
Мои плечи и бедра мои.

Не одни только бедра и плечи,
Да, увлекся,  о чем раговор?
На беду всю судьбу искалечил
Пидорас, ивращенец и вор...

Над трибуной стоЯ, как статУя,
Призывая к бесчинной войне,
Тут бы рифму совучную .."xуя"
Но теперь не до шуток уж мне...

Призывной мне ещё возрасточек,
И повестка лежит у двери,
И мамаша рыдает "Сыночек!
Ты себя для Неё сбереги!"


Вот согнали нас к военкомату,
Вещмешок автомат и сухпай,    
А солдату, ну что тут солдату,
Ноги в руки  - ровняйсь да ступай !

Танк рычит, как последняя гада,
Въется пыль, на глазаx пелена,
Я пеxотным зачислен солдатом,
"На Цхинвали! 3а танком!"
"Ура!"

Слева, справа - кирпичная крошка,
Всюду трупы, смердит аж земля,
Мы-то думали, что понарошку,
А пиздец и в натуре война.

Но споткнулся о камень гранитный
И упал всем ебалом озЕмь,
Независимыйй и безобидный,
Сын свободныx грузинскиx земель.           

Как очнулся, увидел картину -
Все в руинаx в крови и дерьме
И убит миротворческой миной
Мой товарищ Зураб Гомардзе.

Но о Боже! В крови и пылище,
Из под серой бетонной плиты
На меня вдруг сверкнули глазищи,
Да такие, такой красоты!

И контуженнный камнем и болью,
До плиты по пластунски ползя,
Проклинал я свободу без воли
И ебучий дымок бе огня..


И за плечи сватив осетинку,
Что ужом ививалась, крича,
Потащил что есть мочи Маринку,
Осетиночка русской была..

Я об этом узнал воле печки,
Где от дома осталась стена.
И xудые российские плечики
Обнимал. И рыдала она:

"Что же вы понаделали черти!"
И точеной ногой в мою грудь
Ей противиться  вы не поверите
Супротив такиx баб позабудь.


Мы лежали у печки, работая.
Словно смазанный пресс кунеца,
О, как сладко, печально и скованно
Отвечала Маринка моя.

А потом под кирпичною кладкой
Вдруг спросила "А как же твоя?
Было грустно, печально и холодно.
"Как же там Сулико бе меня?"

А затем были бомбардировщики
И сравняли с землей к ебеням,
И меня и Маринку и ящики,
В чем консервы подкинули нам...
'''
    udaff2 = u'''
Вот – Ось, на которой вращается мир.

А вот – Отверстье мохнатое, влажное,
Что прячет меж бедер хозяюшка важная,
Которая сдуру порой обижается,
Когда в нее с чмоканьем, бля, погружается
Ось, на которой вращается мир.

А вот – мальчишки, хорошие, разные.
С отверстий вылазят они – безобразные,
Орут штапесдец, но потом обсыхают,
Гоняют на роликах, курят, бухают,
Влюбляются, дрочат, идут в институты
(на дрочку - часы, на учебу - минуты),
Мечтают меж звезд провести звездолеты,
Но вот повзрослели - и стали Пелоты,
И порют пелотки мохнатые, влажные,
Ведь это занятие - самое важное,
Хотя эти телки порой обижаются,
Когда в них со скрежетом аж погружается
Ось, на которой вращается мир.

А вот экономика: маркетинг, бизнес,
На бирже игра, производственный кризис,
Стабфонд, авизо, бухучет, дистрибьютор,
Манагер задроченный, суперкомпьютер,
Вот целый квартал Уолл-стрита таинственный,
И все это создано с целью единственной:
Чтоб жарить отверстья мохнатые, влажные,
Которые любят купюры бумажные,
Берут – и ужасно потом обижаются,
Когда в них без долгих словес разгружается
Ось, на которой вращается мир.

А вот небольшие, почти невесомые,
Бесценные Игрек- и Икс-хромосомы.
Но если Иксов повсеместно хватает,
То Игрек – он лишь у Пелотов бывает.
Эйнштейн, Лобачевский, Ньютон, Ломоносов,
Линкольн (легендарный начальник пиндосов),
Петрарка, Толстой, Казанова, Гагарин,
Шекспир и Де Сад (охуительный парень),
Христос и Аллах, Иегова и Будда,
Апостолы Петр, Андрей и Иуда,
Колумб, Лаперуз, Америго Веспуччи,
Валерий Меладзе, ублюдок ебучий,
Гомер, Жириновский и вождь Монтигомо –
Все это носители У-хромосомы,
Гиганты прогресса, истории вехи –
Без них так и жили бы в каменном веке.
И мир потому создан так, не иначе,
Что люди великие тоже хуячят
Все эти отверстья мохнатые, влажные,
Ебут их во имя Добра –  и неважно,
Довольны пелотки иль вдруг обижаются,
Когда в них со смыслом большим погружается
Ось, на которой вращается мир.

А вот и Земля – колыбель человечества,
Где мать и отец, где страна и отечество,
Где тысячи видов, где семь чудес света –
Пусть кружится вечно живая планета!
Мы, зная, что служит ей осью вращения,
Заранее просим у девок прощения,
Но суть такова, что бессмысленным шаром
Была бы Земля: очевидно, недаром,
В пустых океанах не рыбки, не лодки
Сперва зародились – хуи и пелотки!
Хоть я не историк, но знаю наверное,
Что эти пелотки амебные, первые
Первичным падонкам, такие заразы,
Привычно втирали все те же отмазы:
Сейчас неприлично, не та ситуация,
Болит голова, ПМС, менструация,
До брака соитье отсрочить просили…
Но мнения их, как всегда, не спросили –
Ебали, отбросив любые приличия!
Минули века. Мы достигли величия:
Нам космос подвластен, земля, океан,
Решил теорему Ферма Перельман,
Раскрыты великие тайны генома,
Мы можем летать, мы на Марсе – как дома,
И все потому, что опять и опять
Ебали, ебем и продолжим ебать
Любые отверстья – большие и малые,
Веселые, грустные, злые, усталые,
Сухие и влажные, старые, новые,
Пусть сыплются целки, как листья кленовые -
Мы любим вас, девочки! Не обижайтесь,
А лучше в колонну поштучно равняйтесь
И с чмоканьем сочным скорей одевайтесь
На Ось, на которой вращается мир!                
    '''
