import discord
import traceback
import aiosqlite
import datetime
import asyncio
import sqlite3
import random
import sys
from pathlib import Path
from discord.ext import commands

#List/Dict Constants

#.profile rank (game_mode) (game_rank)
game_rank = ['C-','C','C+','B-','B','B+','A-','A','A+','S','S+0','S+1','S+2','S+3','S+4','S+5','S+6','S+7','S+8','S+9',]
game_mode = {'rank': ['rm','sz','tc','cb', 'clamblitz', 'rainmaker', 'splatzones', 'towercontrol'], 'rang': ['og', 'hc', 'tk', 'mc', 'muschelchaos', 'operation-goldfisch', 'hersschaft', 'turm-kommando']}

#.factopedia (subcommand) (arg)
boss_list_reformat = {'octo oven': 'Octo Oven', 'octo samurai': 'Octo Samurai', 'octo shower': 'Octo Shower', 'mighty octostomp': 'Mighty Octostomp', 'dj octavio': 'DJ Octavio',}
boss_list = ['octo oven','octo samurai','octo shower','mighty octostomp','dj octavio',]
shooter_dict = ['Sploosh-o-matic','Neo Sploosh-o-matic','Splattershot Jr.','Custom Splattershot Jr.','Splash-o-matic','Neo Splash-o-matic','Aerospray MG','Aerospray RG','Splattershot','Tentatek Splattershot','Hero Shot Replica','.52 Gal','.52 Gal Deco',"N-Zap '85","N-Zap '89",'Splattershot Pro','Forge Splattershot Pro','.96 Gal','.96 Gal Deco','Jet Squelcher','Custom Jet Squelcher','L-3 Nozzlenose','L-3 Nozzlenose D','H-3 Nozzlenose','H-3 Nozzlenose D','Squeezer','Foil Squeezer',]
blaster_dict = ['Luna Blaster','Luna Blaster Neo','Blaster','Custom Blaster','Hero Blaster Replica','Range Blaster','Custom Range Blaster','Clash Blaster','Clash Blaster Neo','Rapid Blaster','Rapid Blaster Deco','Rapid Blaster Pro','Rapid Blaster Pro Deco',]
charger_dict = ['Squiffer','New Squiffer','Splat Charger','Firefin Splat Charger','Hero Charger Replica','Splatterscope','Firefin Splatterscope','E-liter 4K','Custom E-liter 4K','E-Liter 4K Scope','Custom E-liter 4K Scope','Bamboozler 14 Mk I','Goo Tuber','Custom Goo Tuber',]
roller_dict = ['Carbon Roller','Carbon Roller Deco','Splat Roller','Krak-On Splat Roller','Hero Roller Replica','Dynamo Roller','Gold Dynamo Roller','Flingza Roller','Foil Flingza Roller',]
brush_dict = ['Inkbrush','Inkbrush Noveau','Octobrush','Octobrush Nouveau','Herobrush Replica',]
slosher_dict = ['Slosher','Slosher Deco','Hero Slosher Replica','Tri-Slosher','Tri-Slosher Nouveau','Sloshing Machine','Sloshing Machine Neo',]
splatling_dict = ['Mini Splatling','Zink Mini Splatling','Heavy Splatling','Heavy Splatling Deco','Hero Splatling Replica','Hydra Splatling',]
dualies_dict = ['Dapple Dualies', 'Dapple Dualies Nouveau', 'Splat Dualies', 'Enperry Splat Dualies', 'Hero Dualie replica', 'Glooga Dualies', 'Glooga Dualies Nouveau', 'Dualie Squelchers', 'Dark Tetra Dualies',]
brella_dict = ['Splat Brella', 'Sorella Brella', 'Hero Brella Replica', 'Tenta Brella', 'Undercover Brella',]
weapon_cagetory = ['shooter', 'blaster', 'charger', 'roller', 'brush', 'slosher', 'splatling', 'dualies', 'brella',]

#.metro defend-orb
enemy_choice = ['<:octozeppelin:459743817265053696>', '<:octomissle:459743809493008385> ']

#Mem Viewer Poem
Mem_Dict = {
  'OctCollectIcon_00': 'At last we meet, my so-called foe. But is our fate to spray this hate? Perhaps well learn in depths below... ',
  'OctCollectIcon_01': 'You gaze seaward with azure hope. Between each blink you calmly think, As when you use a Splatterscope. ',
  'OctCollectIcon_02': 'The rolling column splatters all. A stray shot shakes the trees awake. The summer turns, here comes the fall. ',
  'OctCollectIcon_03': 'You paint the turf with graceful strokes. With watchful eye, I breathe a sigh. From snipers perch, I go for broke. ',
  'OctCollectIcon_04': 'With tresses pink and eyes a blank, A smile so faint, it hides your feint, You slip on past—outfoxed! Outflanked! ',
  'OctCollectIcon_05': 'The world I knew seems like a trap. Im drawn now to the strange and new. Would my old friends think me a sap? ',
  'OctCollectIcon_06': 'Two fat and heavy locks hang low. They frame your face above a base Of stumpy leg and pigeon toe. ',
  'OctCollectIcon_07': 'A hilltop picnic, friends and fruit. Your whirling blades provide us shade. I raise a hand in mock salute. ',
  'OctCollectIcon_08': 'Destroy your troubles—bombs away! A tempting thought: bring all to naught. No wonder your friends tend to stray. ',
  'OctCollectIcon_09': 'You face away, thinking me blind, Like I dont know what you wont show. Your love is still clear from behind. ',
  'OctCollectIcon_10': 'So principled you might explode, But when you burst, whos really cursed? Your loved ones have to bear that load. ',
  'OctCollectIcon_11': 'It seems to you a sly attack, But for your pains you make no gains. You only get shot in the back. ',
  'OctCollectIcon_12': 'How loftily you float on high, Suspended there in starry air As you drip purple passing by. ',
  'OctCollectIcon_13': 'How desolate this star-marked limb. Is what awaits me this same fate? I must not dwell; its much too grim. ',
  'OctCollectIcon_14': 'Though parted by the ocean deep, My oldest friend, we meet again. I touch your face; you rouse from sleep. ',
  'OctCollectIcon_15': 'You overwhelm with crowds and throngs. At every turn, you writhe and churn. Why cant we simply get along? ',
  'OctCollectIcon_16': 'Where love could blossom, spite congeals. Faced with these thieves, I aim and heave A cluster bomb right in the feels. ',
  'OctCollectIcon_17': 'The hunt leads down a winding path. Tightly coiled and well-oiled, These dirty squids could use a bath. ',
  'OctCollectIcon_18': 'Now nights grow long; summer abates. The tides recede as squids stampede. With fireworks, we celebrate. ',
  'OctCollectIcon_19': 'Erupting eel glimpses the sky. Its eyelids squint against the glint Of sun unseen by creatures shy. ',
  'OctCollectIcon_20': 'When problems stack too tall to see, Just chip away and, day by day, Youll grow to live a life carefree. ',
  'OctCollectIcon_21': 'Your motor whines; the ocean roars. No ink can halt your firm assault. Let these invaders know the score. ',
  'OctCollectIcon_22': 'A sudden drizzle bars my way. Its no hour for this shower, But light rain wont ruin my day. ',
  'OctCollectIcon_23': 'Each glittered scale shines so bright. Youre my last ditch to strike it rich And tilt my bank balance aright.',
  'OctCollectIcon_24': 'Finalitys not what it seems. When your end comes, rise up and run. Dont let defeat dissolve your dreams. ',
  'OctCollectIcon_25': 'Oblivious, adrift, and round, You hold inside a tempting prize. Who doesnt love that popping sound? ',
  'OctCollectIcon_26': 'You teach the virtues of the still, And yet I spurned the lesson learned. My problem is I have no chill',
  'OctCollectIcon_27': 'Another squid? Im gonna hurl. Its just litter! Please consider How we Octolings see the world. ',
  'OctCollectIcon_28': 'Were torn apart so many times; I must be bold and keep my hold To make their team pay for their crimes. ',
  'OctCollectIcon_29': 'When four are one, they make a team. But one from ten? Uhh, come again? Its like some kind of fever dream. ',
  'OctCollectIcon_30': 'I topple from the tower ledge And choke back tears to see the gears Eliminate our hard-won edge. ',
  'OctCollectIcon_31': 'To plant a trees its own reward. After youre gone, it will grow on In memory, initials scarred. ',
  'OctCollectIcon_32': 'The polished nozzle gleams and shines. Unblemished gun reflects the sun. A good days match; victorys mine. ',
  'OctCollectIcon_33': 'I shake the squeegee to and fro. As I do laps my color saps; A fair trade for a mighty blow. ',
  'OctCollectIcon_34': 'Closer to pyramids than spheres— Let fly the bombs! A sigh, then calm. A pillow stained with ink—or tears. ',
  'OctCollectIcon_35': 'Though it flies errant or amiss, Should its sly arc hit near the mark, Your fate is sealed with its kiss. ',
  'OctCollectIcon_36': 'Not everyone can be a scourge In tense combat. I toss this splat, A monument to my last surge. ',
  'OctCollectIcon_37': 'Its friendly face, its easy stride— Thats all a front. Let me be blunt; It leaves you with nowhere to hide. ',
  'OctCollectIcon_38': 'No stealth or guile, not for you. You pave the way as plain as day, Foreshadowing imminent spew. ',
  'OctCollectIcon_39': 'The sickly sweet aroma spreads. Its stagnant arms bring only harm, Along with sluggish, looming dread. ',
  'OctCollectIcon_40': 'I watch your tendrils undulate; A blue bouquet that twirls and sways, As central mass swells and deflates. ',
  'OctCollectIcon_41': 'Black, bulging eyes stare far inside. What does he see deep within me? From his sharp gaze, no one can hide. ',
  'OctCollectIcon_42': 'Two friends who never are apart: Ones always cool, the other stews. I love them both with all my heart. ',
  'OctCollectIcon_43': 'A patch of sun? A fresh-caught fish? No bribe will swerve your eye for turf, However desperately we wish. ',
  'OctCollectIcon_44': 'Hmm, Slosher? Inkbrush? Curling Bomb? Id gladly browse for hours and hours; Your gushing ramble brings me calm. ',
  'OctCollectIcon_45': 'How long must I wait in his line? Such tragic lack of Crusty snack... Im almost there! It will be mine! ',
  'OctCollectIcon_46': 'They told me you had gone to ground, And your rad groove was concrete proof That you had made it safe and sound. ',
  'OctCollectIcon_47': '"I rule," you said, "Its in my blood. Dont step to me—ESPECIALLY if you cant hang with my best bud." ',
  'OctCollectIcon_48': 'Behind his dour, one-eyed stare, Our urchin friend conceals a yen For making the most out of gear. ',
  'OctCollectIcon_49': 'Oh, what Id give to be employed! Better, Id say, to work for pay Than ride this subway through the void. ',
  'OctCollectIcon_50': 'Our sweat dripping from every pore. The harsh, hot sun wont stop this run. We grit our teeth and ask for more. ',
  'OctCollectIcon_51': 'Squids often wear this as they strike With bomb and brush. Its quite a rush. Wish I could know what that was like... ',
  'OctCollectIcon_52': 'I hate the sea but love the breeze. The sandy shore I will endure Just for that brisk, zephyrous tease. ',
  'OctCollectIcon_53': 'Constructed of glass and concrete, A city stays in dull, drab grays Till we splash color on its streets. ',
  'OctCollectIcon_54': 'Your tude is righteous, as you say. Is your science as defiant? Prove that your battle rhymes can slay',
  'OctCollectIcon_55': 'Put down the phone; go shelve your book. Get ready, champ—its time to camp! Well share a drink right from the brook! ',
  'OctCollectIcon_56': 'I see you standing in the rain. Within a storm—forever warm. Powerful as a hurricane. ',
  'OctCollectIcon_57': 'A Skalop brand atop your crown Will turn some heads but really shreds When it is simply turned around. ',
  'OctCollectIcon_58': 'I pack my feelings in a box: A parcel stuffed with hope and love And trimmed with stamps unorthodox. ',
  'OctCollectIcon_59': '"When going through here, play it cool!" Or get a clue and dont go through! I wont bend on this! Thems the rules! ',
  'OctCollectIcon_60': 'How I admire Lil Max! The highest rank to be so swank That my rivals have heart attacks. ',
  'OctCollectIcon_61': 'Mistakes of youth teach us a lot. We skate too fast or have a blast And learn quickly not to get caught. ',
  'OctCollectIcon_62': 'Ive seen this, but Im not aware Just what the splat Im looking at! Is it a frog or a brown bear? ',
  'OctCollectIcon_63': 'Your song inspired a blush of love. It gave my heart a fresh new start. Now I ascend to shores above. ',
  'OctCollectIcon_64': 'The tides go out and take the light. How will I greet you when we meet? It keeps me up on inkstained nights. ',
  'OctCollectIcon_65': 'Encased in sturdy sphere of glass. It breaks my heart to see you caught With whiskers trembling as I pass. ',
  'OctCollectIcon_66': 'The rhythm etched in little jolts; Those idols sing and put a spring In my steps as I crank the volts. ',
  'OctCollectIcon_67': 'Though slick with slime, I keep my grip. The chill seeps through my gift from you. I mustnt let this cargo slip. ',
  'OctCollectIcon_68': 'Beneath a summer sky I walk, Through valley, plain, and back again, Dreaming of what you might unlock. ',  
  'OctCollectIcon_69': 'When I get my hands on these fish I might exchange them on the range, Except that they look so delish... ',
  'OctCollectIcon_70': 'A mystery rolled up and bound— Oh, whats the use? Its too obtuse. Ill dump it in the lost and found. ',
  'OctCollectIcon_71': 'I leave without ceremony. Dont be too sore; I wanted more. My sincerest apology. ',
  'OctCollectIcon_72': 'I see you walking down the street. You think youre slick in those lime kicks, But theyd look fresher on my feet.',
  'OctCollectIcon_73': 'On colder days, I like these clothes. With other threads Id stay in bed— Its too frigid to be exposed! ',
  'OctCollectIcon_74': 'This swells a stir of royal pride. In small or large, you lead the charge. The ink of nobles flows inside. ',
  'OctCollectIcon_75': 'Such devilfish-may-care couture— The colors clash and make a splash! Without a doubt, footwear du jour.',
  'OctCollectIcon_76': 'No matter thickness, brim, or gauge, A well-done purl will awe the world. These handmade hats are all the rage! ',
  'OctCollectIcon_77': 'I dont quite trust this stark white brand. Its more for squids or little kids... And wheres the pop? Its oh-so bland! ',
  'OctCollectIcon_78': 'The squishing footsteps trudge in muck. Their path revealed by heavy heel. My heart beats quick; a stroke of luck! ',
  'OctCollectIcon_79': 'It keeps the elements away: No rain, nor heat, nor wind, nor sleet. But does it guard against ink spray? ',
}

Mem_Name = {
  'OctCollectIcon_00': 'Inkling Squid',
  'OctCollectIcon_01': 'Inkling Boy (Blue)',
  'OctCollectIcon_02': 'Inkling Boy (Green)',
  'OctCollectIcon_03': 'Inkling Girl (Orange)',
  'OctCollectIcon_04': 'Inkling Girl (Pink)',
  'OctCollectIcon_05': 'Octarian',
  'OctCollectIcon_06': 'Twintacle Octotrooper',
  'OctCollectIcon_07': 'Octocopter',
  'OctCollectIcon_08': 'Octobomber',
  'OctCollectIcon_09': 'Tentakook',
  'OctCollectIcon_10': 'Octopod',
  'OctCollectIcon_11': 'Octostamp',
  'OctCollectIcon_12': 'Octozeppelin',
  'OctCollectIcon_13': 'Tentacle',
  'OctCollectIcon_14': 'Octoling',
  'OctCollectIcon_15': 'Chum',
  'OctCollectIcon_16': 'Steelhead',
  'OctCollectIcon_17': 'Steel Eel',
  'OctCollectIcon_18': 'Flyfish',
  'OctCollectIcon_19': 'Maws',
  'OctCollectIcon_20': 'Stinger',
  'OctCollectIcon_21': 'Scrapper',
  'OctCollectIcon_22': 'Drizzler',
  'OctCollectIcon_23': 'Goldie',
  'OctCollectIcon_24': 'Spawn Point',
  'OctCollectIcon_25': 'Balloon',
  'OctCollectIcon_26': 'Bumper',
  'OctCollectIcon_27': 'Squid Bumper',
  'OctCollectIcon_28': 'Rainmaker',
  'OctCollectIcon_29': 'Power Clam ',
  'OctCollectIcon_30': 'Tower',
  'OctCollectIcon_31': 'Tree',
  'OctCollectIcon_32': 'Splattershot',
  'OctCollectIcon_33': 'Splat Roller',
  'OctCollectIcon_34': 'Splat Bomb',
  'OctCollectIcon_35': 'Suction Bomb',
  'OctCollectIcon_36': 'Burst Bomb',
  'OctCollectIcon_37': 'Autobomb',
  'OctCollectIcon_38': 'Curling Bomb',
  'OctCollectIcon_39': 'Toxic Mist',
  'OctCollectIcon_40': 'Jelfonzo',
  'OctCollectIcon_41': 'Bisk',
  'OctCollectIcon_42': 'Flow',
  'OctCollectIcon_43': 'Judd & Lil Judd',
  'OctCollectIcon_44': 'Sheldon',
  'OctCollectIcon_45': 'Crusty Sean',
  'OctCollectIcon_46': 'Marina',
  'OctCollectIcon_47': 'Pearl',
  'OctCollectIcon_48': 'Murch',
  'OctCollectIcon_49': 'Mr. Grizz',
  'OctCollectIcon_50': 'Tentatek',
  'OctCollectIcon_51': 'SquidForce',
  'OctCollectIcon_52': 'Zekko',
  'OctCollectIcon_53': 'Toni Kensa',
  'OctCollectIcon_54': 'Firefin',
  'OctCollectIcon_55': 'Inkline',
  'OctCollectIcon_56': 'Zink',
  'OctCollectIcon_57': 'Skalop',
  'OctCollectIcon_58': 'iShipIt Logo',
  'OctCollectIcon_59': '"Slow Your Roll" Mole',
  'OctCollectIcon_60': 'Lil Max',
  'OctCollectIcon_61': 'Jr. Mark',
  'OctCollectIcon_62': 'Familiar Grafitti',
  'OctCollectIcon_63': 'Callie',
  'OctCollectIcon_64': 'Marie',
  'OctCollectIcon_65': 'Zapfish',
  'OctCollectIcon_66': 'Mini Zapfish',
  'OctCollectIcon_67': 'Power Egg',
  'OctCollectIcon_68': 'Key',  
  'OctCollectIcon_69': 'Sardinium',
  'OctCollectIcon_70': 'Sunken Scroll',
  'OctCollectIcon_71': 'DJ Octavio',
  'OctCollectIcon_72': 'Mint Dakroniks',
  'OctCollectIcon_73': 'Skalop Hoodie',
  'OctCollectIcon_74': 'King Tank',
  'OctCollectIcon_75': 'Orange Arrows',
  'OctCollectIcon_76': 'Knitted Hat',
  'OctCollectIcon_77': 'White Tee',
  'OctCollectIcon_78': 'Neon Sea Slugs',
  'OctCollectIcon_79': 'Takoroka Mesh',
}

#Vending Machine
R_List = ['https://cdn.discordapp.com/attachments/460978785697923072/468225827897737266/Great-Zapfish.png', 'https://cdn.discordapp.com/attachments/460978785697923072/468225829931974658/Sniper.png', 'https://cdn.discordapp.com/attachments/460978785697923072/468225830758252544/Squid-Sisters-Traditional.png', 'https://cdn.discordapp.com/attachments/460978785697923072/468225833228828683/Squid-VS-Octopus.png', 'https://cdn.discordapp.com/attachments/466777024925663232/466796669124739083/pearl_and_marina_banner_v100.png', 'https://cdn.discordapp.com/attachments/455987115407441921/464837415010304011/ineedsleep.png', 'https://cdn.discordapp.com/attachments/455987115407441921/464837417145335820/7-1.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248771092283392/banner2.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248772501307402/banner3.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248774615367700/banner4.png', 'https://cdn.discordapp.com/attachments/455987115407441921/463095338308468736/banner6.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248777169698826/SplatBanner_S1.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460260394456317952/banner5.png', 'Agent', 'Grizzco-Employee', 'Veemo', 'Weyo', 'Squid-Sisters-Fan', 'Squid', 'Off-The-Hook-Fan',]
Item_Name = {'https://cdn.discordapp.com/attachments/460978785697923072/468225827897737266/Great-Zapfish.png': 'Great-Zapfish', 'https://cdn.discordapp.com/attachments/460978785697923072/468225829931974658/Sniper.png': 'Charger-Squid', 'https://cdn.discordapp.com/attachments/460978785697923072/468225830758252544/Squid-Sisters-Traditional.png': 'Squid-Sisters-Traditional', 'https://cdn.discordapp.com/attachments/460978785697923072/468225833228828683/Squid-VS-Octopus.png': 'Squid-VS-Octopus', 'https://cdn.discordapp.com/attachments/466777024925663232/466796669124739083/pearl_and_marina_banner_v100.png': 'Off-The-Hook-Special', 'https://cdn.discordapp.com/attachments/455987115407441921/464837415010304011/ineedsleep.png': 'Squid-Sisters-Special', 'https://cdn.discordapp.com/attachments/455987115407441921/464837417145335820/7-1.png': 'Squids', 'https://cdn.discordapp.com/attachments/455987115407441921/463095338308468736/banner6.png': 'Octo-Expansion-Special (Banner)', 'https://cdn.discordapp.com/attachments/458442870873915392/460248771092283392/banner2.png': 'Splatoon 2 (Banner)', 'https://cdn.discordapp.com/attachments/458442870873915392/460248772501307402/banner3.png': 'Squid Sisters (Banner)', 'https://cdn.discordapp.com/attachments/458442870873915392/460248774615367700/banner4.png': 'Off the Hook (Banner)', 'https://cdn.discordapp.com/attachments/458442870873915392/460248777169698826/SplatBanner_S1.png': 'Splatoon 1 (Banner)', 'https://cdn.discordapp.com/attachments/458442870873915392/460260394456317952/banner5.png': 'Salmon-Run (Banner)', 'Agent': 'Agent', 'Grizzco-Employee': 'Grizzco-Employee', 'Veemo': 'Veemo', 'Weyo': 'Weyo', 'Squid-Sisters-Fan': 'Squid-Sisters-Fan', 'Squid': 'Squid', 'Off-The-Hook-Fan': 'Off-The-Hook-Fan'}
R_List_Banner = ['https://cdn.discordapp.com/attachments/460978785697923072/468225827897737266/Great-Zapfish.png', 'https://cdn.discordapp.com/attachments/460978785697923072/468225829931974658/Sniper.png', 'https://cdn.discordapp.com/attachments/460978785697923072/468225830758252544/Squid-Sisters-Traditional.png', 'https://cdn.discordapp.com/attachments/460978785697923072/468225833228828683/Squid-VS-Octopus.png', 'https://cdn.discordapp.com/attachments/466777024925663232/466796669124739083/pearl_and_marina_banner_v100.png', 'https://cdn.discordapp.com/attachments/455987115407441921/464837415010304011/ineedsleep.png', 'https://cdn.discordapp.com/attachments/455987115407441921/464837417145335820/7-1.png', 'https://cdn.discordapp.com/attachments/455987115407441921/463095338308468736/banner6.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248771092283392/banner2.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248772501307402/banner3.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248774615367700/banner4.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460248777169698826/SplatBanner_S1.png', 'https://cdn.discordapp.com/attachments/458442870873915392/460260394456317952/banner5.png']
Banner_Set = {'great-zapfish': 'https://cdn.discordapp.com/attachments/460978785697923072/468225827897737266/Great-Zapfish.png', 'charger-squid': 'https://cdn.discordapp.com/attachments/460978785697923072/468225829931974658/Sniper.png', 'squid-sisters-traditional': 'https://cdn.discordapp.com/attachments/460978785697923072/468225830758252544/Squid-Sisters-Traditional.png', 'squid-vs-octopus': 'https://cdn.discordapp.com/attachments/460978785697923072/468225833228828683/Squid-VS-Octopus.png', 'off-the-hook-special': 'https://cdn.discordapp.com/attachments/466777024925663232/466796669124739083/pearl_and_marina_banner_v100.png', 'squid-sisters-special': 'https://cdn.discordapp.com/attachments/455987115407441921/464837415010304011/ineedsleep.png', 'squids': 'https://cdn.discordapp.com/attachments/455987115407441921/464837417145335820/7-1.png', 'splatoon-2': 'https://cdn.discordapp.com/attachments/458442870873915392/460248771092283392/banner2.png', 'squid-sisters': 'https://cdn.discordapp.com/attachments/458442870873915392/460248772501307402/banner3.png', 'off-the-hook': 'https://cdn.discordapp.com/attachments/458442870873915392/460248774615367700/banner4.png', 'splatoon-1': 'https://cdn.discordapp.com/attachments/458442870873915392/460248777169698826/SplatBanner_S1.png', 'salmon-run': 'https://cdn.discordapp.com/attachments/458442870873915392/460260394456317952/banner5.png', 'octo-expansion-special': 'https://cdn.discordapp.com/attachments/455987115407441921/463095338308468736/banner6.png',}
Banner_Name = ['Great-Zapfish', 'Squid-Sisters-Traditional', 'Charger-Squid', 'Squid-VS-Octopus', 'Off-The-Hook-Special', 'Squid-Sisters-Special', 'Squids', 'Splatoon-2', 'Splatoon-1', 'Squid-Sisters', 'Off-The-Hook', 'Salmon-Run', 'Octo-Expansion-Special', 'Octo-Expansion']
Banner_Name_RE = {'charger-squid': 'Charger-Squid', 'great-zapfish': 'Great-Zapfish', 'squid-sisters-traditional': 'Squid-Sisters-Traditional', 'squid-vs-octopus': 'Squid-VS-Octopus', 'off-the-hook-special': 'Off-The-Hook-Special', 'squid-sisters-special': 'Squid-Sisters-Special', 'squids': 'Squids', 'octo-expansion-special': 'Octo-Expansion-Special', 'splatoon-2': 'Splatoon-2', 'splatoon-1': 'Splatoon-1', 'squid-sisters': 'Squid-Sisters', 'off-the-hook': 'Off-The-Hook', 'salmon-run': 'Salmon-Run'}
Title_Set = ['off-the-hook-fan', 'agent', 'grizzco-employee', 'veemo', 'weyo', 'squid-sisters-fan', 'squid']
Title_Set_RE = {'off-the-hook-fan': 'Off-The-Hook-Fan', 'agent': 'Agent', 'grizzco-employee': 'Grizzco-Employee', 'veemo': 'Veemo', 'weyo': 'Weyo', 'squid-sisters-fan': 'Squid-Sisters-Fan', 'squid': 'Squid'}
Item_Int = {'https://cdn.discordapp.com/attachments/458442870873915392/460248771092283392/banner2.png': '0', 'https://cdn.discordapp.com/attachments/458442870873915392/460248772501307402/banner3.png': '1', 'https://cdn.discordapp.com/attachments/458442870873915392/460248774615367700/banner4.png': '2', 'https://cdn.discordapp.com/attachments/458442870873915392/460248777169698826/SplatBanner_S1.png': '3', 'https://cdn.discordapp.com/attachments/458442870873915392/460260394456317952/banner5.png': '4', 'Agent': '5', 'Grizzco-Employee': '6', 'Veemo': '7', 'Weyo': '8', }


#SubIcon
Sub_Icon = {'Sub Power Up': '<:S2_Ability_Sub_Power_Up:462474819603005450>', 'Toxic Mist': '<:S2_Weapon_Sub_Toxic_Mist:461273839108620289>', 'Suction Bomb': '<:S2_Weapon_Sub_Suction_Bomb:461273839020539915>', 'Squid Beakon': '<:S2_Weapon_Sub_Squid_Beakon:461273839217672222>', 'Sprinkler': '<:S2_Weapon_Sub_Sprinkler:461273838877933569>', 'Splat Bomb': '<:S2_Weapon_Sub_Splat_Bomb:461273838928265219>', 'Splash Wall': '<:S2_Weapon_Sub_Splash_Wall:461273838575943692>', 'Point Sensor': '<:S2_Weapon_Sub_Point_Sensor:461273838571749387>', 'Ink Mine': '<:S2_Weapon_Sub_Ink_Mine:461273838894841866>', 'Curling Bomb': '<:S2_Weapon_Sub_Curling_Bomb:461273838794309653>', 'Burst Bomb': '<:S2_Weapon_Sub_Burst_Bomb:461273838630469673>', 'Autobomb': '<:S2_Weapon_Sub_Autobomb:461273839670657035>',}
#SpecialIcon
Special_Icon = {'Tenta Missiles': '<:S2_Weapon_Special_Tenta_Missiles:461275575210868737>', 'Sting Ray': '<:S2_Weapon_Special_Sting_Ray:461275575412195328>', 'Splat-Bomb Launcher': '<:S2_Weapon_Special_SplatBomb_Laun:461275575365926913>', 'Splashdown': '<:S2_Weapon_Special_Splashdown:461275575437361172>', 'Inkjet': '<:S2_Weapon_Special_Inkjet:461275575072325664>', 'Ink Storm': '<:S2_Weapon_Special_Ink_Storm:461275575416389642>', 'Ink Armor': '<:S2_Weapon_Special_Ink_Armor:461275575567515648>', 'Bubble Blower': '<:S2_Weapon_Special_Bubble_Blower:461275575131176963>', 'Baller': '<:S2_Weapon_Special_Baller:461275575282171946>', 'Curling-Bomb Launcher': '<:S2_Weapon_Special_CurlingBom:461277386558930954>', 'Autobomb Launcher': '<:S2_Weapon_Special_Autobomb_L:461277386470850560>', 'Burst-Bomb Launcher': '<:S2_Weapon_Special_Burst_Launcher:462860488758263809>',}
#AbilityIcon
Ability_Icon = {'Swim Speed Up': '<:S2_Ability_Swim_Speed_Up:461246357433221122>', 'Special Saver': '<:S2_Ability_Special_Saver:461246357521432607>', 'Special Power Up': '<:S2_Ability_Special_Power_Up:461246357773090826>', 'Special Charge Up': '<:S2_Ability_Special_Charge_Up:461246357206990861> ', 'Run Speed Up': '<:S2_Ability_Run_Speed_Up:461246357160853505>', 'Quick Super Jump': '<:S2_Ability_Quick_Super_Jump:461246357148270593>', 'Quick Respawn': '<:S2_Ability_Quick_Respawn:461246356963721237>', 'Ink Saver (Sub)': '<:S2_Ability_Ink_Saver_Sub:461246357420638208>', 'Ink Saver (Main)': '<:S2_Ability_Ink_Saver_Main:461246357278031924>', 'Ink Resistance Up': '<:S2_Ability_Ink_Resistance_Up:461246357269643277>', 'Ink Recovery Up': '<:S2_Ability_Ink_Recovery_Up:461246356812726273>', 'Cold-Blooded': '<:S2_Ability_ColdBlooded:461246357450129408>', 'Bomb Defense Up': '<:S2_Ability_Bomb_Defense_Up:461246357018247170>', '???': '<:S2_Ability_Random:461248903212171294>', 'Thermal Ink': '<:S2_Ability_Thermal_Ink:461258798993113098>', 'Tenacity': '<:S2_Ability_Tenacity:461258798850506753>', 'Stealth Jump': '<:S2_Ability_Stealth_Jump:461258798997307412>', 'Respawn Punisher': '<:S2_Ability_Respawn_Punisher:461258799047507988>', 'Opening Gambit': '<:S2_Ability_Opening_Gambit:461258798796111873>', 'Object Shredder': '<:S2_Ability_Object_Shredder:461258799190376448>', 'Ninja Squid': '<:S2_Ability_Ninja_Squid:461258799001632778>', 'Last-Ditch Effort': '<:S2_Ability_LastDitch_Effort:461258799014084639>', 'Haunt': '<:S2_Ability_Haunt:461258798993113128>', 'Drop Roller': '<:S2_Ability_Drop_Roller:461258798640922627>', 'Comeback': '<:S2_Ability_Comeback:461258799010021386>', 'Ability Doubler': '<:S2_Ability_Ability_Doubler:461258798997176361>',}
#BrandIcon

Brand_Icon = {'Zink': '<:S2_Brand_Zink:461252014043562004>', 'Zekko': '<:S2_Brand_Zekko:461252014148681759>', 'Toni Kensa': '<:S2_Brand_Toni_Kensa:461252014098350090>', 'Tentatek': '<:S2_Brand_Tentatek:461252013959938070>', 'Takoroka': '<:S2_Brand_Takoroka:461252014580432907>', 'SquidForce': '<:S2_Brand_SquidForce:461252013993361460>', 'Splash Mob': '<:S2_Brand_Splash_Mob:461252014060470302>', 'Skalop': '<:S2_Brand_Skalop:461252014433763328>', '_Rockenberg': '<:S2_Brand_Rockenberg:461252014135836702>', 'KrakOn': '<:S2_Brand_KrakOn:461252013951287310>', 'Inkline': '<:S2_Brand_Inkline:461252014081572911>', 'Grizzco': '<:S2_Brand_Grizzco:461252014467448832>', 'Forge': '<:S2_Brand_Forge:461252013829783574>', 'Firefin': '<:S2_Brand_Firefin:461252014500872192>', 'Enperry': '<:S2_Brand_Enperry:461252014454603786>', 'Cuttlegear': '<:S2_Brand_Cuttlegear:461252013984972843>', 'Annaki': '<:S2_Brand_Annaki:461252014203076609>', 'Amiibo': '<:S2_Brand_amiibo:461252014429569024>', 'Octo Canyon': '<:S2_Availability_Octo_Canyon:461255139626450945>', 'Salmon Run': '<:S2_Availability_Grizzco:461255140788273202>', 'Octo Expansion': '<:S2_Availability_Octo_Expansion:461254860889784360>', 'CoroCoro Comic': '<:S2_Availabiliy_CoroCoro:461279995352973312>',}

#Invoke_Cost
command_cost = {'8ball': 200, 'one-shot': 500, 'x': 1000}