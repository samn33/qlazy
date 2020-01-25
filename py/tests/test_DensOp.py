# -*- coding: utf-8 -*-
import unittest
import math
import numpy as np
from qlazypy import QState, DensOp

EPS = 1.0e-6

VECTORS_4 = [[(0.36863213668714157-0.4304545832778979j),
              (0.00456880716357648+0.31132201699178846j),
              (-0.19901565882581562+0.5706027733355113j),
              (-0.43203141919177984-0.17329461246350644j)],
             [(-0.06364497729399213+0.16902274625801428j),
              (0.06245292402876544+0.2987878209871568j),
              (0.03337354328794392-0.912035076464779j),
              (0.14117451507074374+0.14613035490096665j)],
             [(-0.49517354695065136-0.0438430052232861j),
              (-0.15269705797162028+0.019968084786556053j),
              (-0.6385234738751507+0.13257311978856617j),
              (-0.4977343476180527+0.23693563216881966j)],
             [(-0.4878991425412435-0.2558630183720352j),
              (0.5245285395266309-0.41253366460257906j),
              (0.32949583538053306-0.3475792334067698j),
              (-0.0966698415381483-0.11158154881938814j)]]
PROBS_4 = [0.4, 0.3, 0.2, 0.1]

VECTORS_2 = [[(0.05863876576548337+0.9215067273590869j),
              (-0.01812894141407051+0.3834816658781116j)],
             [(0.236463536549216+0.05313978984233403j),
              (-0.9652362584457311-0.09787810786808163j)]]
PROBS_2 = [0.7, 0.3]

VECTORS_4_ANOTHER = [[(-0.23171188365029075-0.44976575869295865j),
                      (-0.4652597650581055-0.5878469339203343j),
                      (-0.05410792227523169-0.24477339772389503j),
                      (0.34516577367929535+0.002933219264063293j)],
                     [(0.11459375873289099+0.2892710117812185j),
                      (-0.5525825093102857+0.07313420000980816j),
                      (0.012180914038979626+0.6241467201316626j),
                      (-0.44959174982016836+0.025578642878645554j)],
                     [(0.09580499560657418-0.15317536497827255j),
                      (0.4630864397220132-0.15937454806350682j),
                      (-0.6734359554019572+0.1517443846298623j),
                      (-0.2606190920913556-0.4278373028364584j)],
                     [(-0.02548936579236915-0.42802352248581044j),
                      (0.03816251984132599-0.0161758808267428j),
                      (-0.1557285570581273+0.40279653530995113j),
                      (0.4201171044723051+0.6718878668184746j)]]
PROBS_4_ANOTHER = [0.5, 0.3, 0.1, 0.1]

VECTORS_2_ANOTHER = [[(0.9444967465104553+0.30011583068496184j),
                      (-0.11293086254868676-0.071435315408065j)],
                     [(-0.09982677944785712+0.70197064935557j),
                      (0.03579114981179062+0.7042661536262684j)]]
PROBS_2_ANOTHER = [0.6, 0.4]

VECTORS_8 = [[(0.09577032330213918+0.32578693176659534j),
              (0.17293965688928617-0.16703777280518783j),
              (0.2522833094366221-0.34338886335367935j),
              (-0.10419132428330434-0.05189538079216872j),
              (-0.22239410689438077+0.08557975180735292j),
              (0.13784951664594144-0.06028723481207203j),
              (-0.050777528779555825-0.20930439172885917j),
              (-0.7103604176103298+0.036752607280013526j)],
             [(-0.432783163056468+0.11182177645338617j),
              (-0.3697180222757764-0.326854239411272j),
              (0.2803206315318449-0.2164859404343351j),
              (0.1545226096475472+0.23650482078504684j),
              (0.16258601762368755-0.2806824957505182j),
              (-0.07941774147603725+0.18645414692427653j),
              (0.1905660490482667+0.40520247256510067j),
              (-0.06128529851558924+0.029366213634755143j)],
             [(0.502493356075487-0.05006738738485411j),
              (0.11856482005974421-0.26033607812564585j),
              (0.14811214369520703-0.12991842378982052j),
              (-0.005440081672453426+0.06532711590537911j),
              (0.21478642795648814-0.27434283591384007j),
              (0.36535178718275946+0.1937968883049974j),
              (-0.46133397004048193-0.32973467785339566j),
              (0.054622297009701025+0.05544379668426229j)],
             [(0.2074293592794887-0.06098882639289186j),
              (0.1637952911172082+0.24658814630448156j),
              (-0.47233821079474314+0.03955204607086354j),
              (-0.08067463986162224+0.09524370212532735j),
              (-0.5849355983467996+0.04434758252672499j),
              (0.32044389718306976+0.08093995295079826j),
              (-0.022064258850711737+0.008284949054818507j),
              (-0.2642057225059104+0.31884045762476465j)],
             [(0.3120640622652051+0.055689917750109334j),
              (-0.13350524066556194+0.22974044169633126j),
              (-0.38912036907545955-0.016493186942529336j),
              (0.40359119035523894+0.6149705428194604j),
              (0.17470548529189361+0.1389663164689407j),
              (-0.2070511787598815+0.11356792040257412j),
              (-0.12235506240024087+0.1055471272771995j),
              (-0.03238040997891213+0.05820717102113558j)],
             [(-0.06708006457220073-0.07839652827186706j),
              (0.19505298417472344-0.12523624531461633j),
              (-0.3153611133878992-0.4034078598899199j),
              (-0.11949699716832679-0.07762700509095462j),
              (0.5241205798013023-0.24073054931611082j),
              (0.2286151291222125+0.20751592686433862j),
              (0.07209658417091415+0.17328500772202257j),
              (-0.41429904429991943-0.13519549488314525j)],
             [(-0.2175799412701267+0.09987253174563442j),
              (-0.059222279454769246+0.16325463733285162j),
              (0.05690000778688471-0.20548364310193215j),
              (0.09185464686063431-0.13339554702186315j),
              (-0.4641018271676363-0.3721982374630525j),
              (-0.06322277828261216-0.1518336996921815j),
              (0.3654043783513319+0.11703054031491696j),
              (0.19517682457365015-0.5239744068550053j)],
             [(0.19897009435663393-0.15027912210425853j),
              (-0.3920630110574348+0.10945027117268202j),
              (0.2639641497120706+0.21435636437567385j),
              (0.04720900146847393-0.2399590956908437j),
              (0.02010750350101476-0.17687896471111597j),
              (-0.21123787292004004+0.15354632141515231j),
              (0.32687606217694576+0.39043374502721606j),
              (0.37336777438159385-0.31324301101368934j)]]
PROBS_8 = [0.2, 0.125, 0.125, 0.125, 0.125, 0.1, 0.1, 0.1]

VECTORS_16 = [[(-0.10341887565116092+0.13070867587948778j),
               (-0.3185305396785478-0.13211927048674127j),
               (-0.2072573707613661-0.5481055072854439j),
               (-0.3038106014654534-0.1169417282582179j),
               (0.011023491134664654-0.22473381357962213j),
               (-0.0038996098958141573-0.16901002673204427j),
               (0.0728298227688442+0.09626363833259498j),
               (0.23140229545581623+0.06242115961012982j),
               (-0.2479571495607666+0.08300147896900474j),
               (-0.1552019163697857-0.1027000331061015j),
               (0.12707704543853734-0.12020123997776433j),
               (0.02702048017458636+0.09698294957171372j),
               (0.011114639400689933+0.13994328389519964j),
               (0.023359204044259303+0.13085991476357756j),
               (-0.06422239057618533-0.09489661539054604j),
               (-0.1327490263226186+0.2021408179809029j)],
              [(0.24470116351032734+0.002562959969051913j),
               (-0.22798346093030805+0.11728251727465656j),
               (-0.06973257988551597+0.15538274758206588j),
               (0.016021181817580745-0.14720031117802054j),
               (-0.49117960664731963+0.029081548764020217j),
               (0.16922716134676272+0.28865178928075064j),
               (0.10681647053820802-0.11285588636102895j),
               (-0.07140504143410001-0.19252482024144352j),
               (-0.17069617661379446+0.07052150985298973j),
               (-0.07615540805419252-0.3090832716875071j),
               (0.05032542955067513+0.43446025001529953j),
               (0.11088784617948838+0.06960528574821412j),
               (-0.015240796290108825-0.08326479151719261j),
               (0.05177410587772698+0.08844626005999241j),
               (0.02531185994376676+0.09390642785937911j),
               (-0.1657444294587517+0.06789460295246144j)],
              [(0.3418365283959861+0.29777571207264303j),
               (-0.05652678638344081-0.3076632229411758j),
               (0.05463647751265424+0.22450090279458737j),
               (0.09893191383973413+0.012134005483036668j),
               (0.040350476658336604+0.029148823046275488j),
               (0.026030000930037142-0.10145536347112065j),
               (0.2914030289648913-0.1134779773112372j),
               (-0.12473739538340547-0.1404849024932321j),
               (-0.2409143140499684+0.019654126923729018j),
               (0.10659838745812236-0.11419712071917626j),
               (-0.11317579096790945-0.07452444704078218j),
               (-0.07483297550901415-0.24711107076330063j),
               (-0.025721183901511634-0.034966321166354584j),
               (-0.00278737926010994-0.25622829243642453j),
               (0.40528216055272237+0.24042764160434174j),
               (0.04441769374092108+0.1653309094684251j)],
              [(-0.060980933863042264+0.047419837650943535j),
               (-0.00047259039878311737-0.08743118172466169j),
               (0.06375296177038008+0.23206639628352674j),
               (-0.2559532946227249+0.22610840311767869j),
               (-0.06838286245141113+0.3321236510790506j),
               (-0.08318052236131687-0.04077385434689264j),
               (0.09221010235959749+0.49310355228775987j),
               (-0.2639430151037718+0.090908209793606j),
               (0.23898119273097393+0.25608404514603966j),
               (-0.08743411572726595+0.040243938983745044j),
               (0.19209824450190538+0.08741433312727027j),
               (-0.3065105791905831-0.11600990661833535j),
               (-0.033516161401340436-0.008056202542534361j),
               (-0.14636634818345295-0.14299677483625656j),
               (0.01592889363734784-0.13615322992900447j),
               (0.10877383147611167+0.03310650466736884j)],
              [(-0.14799570319686994-0.24097697078181737j),
               (-0.4168288340463925-0.1369358637405135j),
               (-0.11260641079220793-0.04364977440825142j),
               (-0.2231295405838708+0.06722006160354238j),
               (0.20306139465369324+0.011106534077611065j),
               (-0.07059041409327912-0.0074995003231093345j),
               (0.24935756092802705-0.09879280673848173j),
               (-0.01103694508404076-0.2271628723912548j),
               (0.1523849774334909-0.13127809670901935j),
               (-0.17106751462442096-0.040066593416448304j),
               (0.19650647539464783-0.21292516781088094j),
               (-0.13319436212834812+0.2591235377820862j),
               (0.2252754104866549+0.16528452920516704j),
               (-0.0136894595770925+0.1867945788195275j),
               (0.2350408039575946+0.16250262535355417j),
               (0.22030175049085085-0.0713045388154052j)],
              [(-0.2617383990279938-0.08991144331925838j),
               (0.03423309789193922-0.036336187099413816j),
               (0.022630382332965406-0.011032005020605834j),
               (-0.07263530374245775-0.1047732036670567j),
               (-0.13854993571280008+0.11549578576990996j),
               (0.21102140753412524+0.3147937630149764j),
               (-0.32757360218475173+0.3368084899279434j),
               (-0.05272376657733856+0.19565961033931498j),
               (0.2864135789828037+0.13164332998795555j),
               (-0.232631982552955-0.323705931670441j),
               (0.21602170478338248+0.0372389088260406j),
               (0.1238204598140784+0.021657380736022268j),
               (-0.22091486764197144+0.03337952384084341j),
               (-0.03889374729498418+0.11135804651035677j),
               (-0.04160931274663184+0.013896252109396335j),
               (0.08158640664882572+0.26745453721093193j)],
              [(-0.11558537675740688-0.21065174006578702j),
               (0.2686250596956003+0.27403270556127224j),
               (-0.13969594643478772+0.2148631258089769j),
               (0.018668293098777034+0.04311791944059699j),
               (-0.40457175510428783-0.014925912933801216j),
               (0.0362932847107504+0.05022024457813735j),
               (0.014354160710372276-0.16469443391912422j),
               (-0.1102804886539672-0.036124435116574406j),
               (0.3705485586246982+0.055466393891743404j),
               (0.08412562486718288-0.018614471040197936j),
               (-0.340103022870028-0.3396739251781766j),
               (-0.011691038800325737+0.08467106925720286j),
               (0.03125133494274408+0.07012024024662974j),
               (-0.09433134493676047-0.014150161052934757j),
               (0.1711352297871593-0.1747630512943818j),
               (-0.125943070863537-0.20430970895398412j)],
              [(0.08709119561420885-0.09650366574390522j),
               (-0.16044321988682403+0.20098920876964632j),
               (0.01478017526338273-0.3324716404329413j),
               (0.11165016833514368-0.17248475110722525j),
               (0.2482994849507584-0.06088806980674369j),
               (-0.012291678097043473+0.06629715057950318j),
               (-0.1325003287314334+0.22517209497168406j),
               (0.0018384507884904274-0.32921959597446254j),
               (-0.05867731013076784-0.040517521301627155j),
               (0.13015286369505588-0.31574598558650757j),
               (-0.2484090180167875-0.0993879817438549j),
               (-0.27409782396812193-0.2947577321411428j),
               (-0.07401548422371922-0.11980532594942385j),
               (-0.32973795434220604-0.034102336550870575j),
               (-0.050065142538148456-0.05006782358433667j),
               (-0.07710268698614559-0.14642471035490884j)],
              [(-0.23891518119791733-0.24963065234845064j),
               (0.11186303257623081+0.15945617332594864j),
               (-0.25530287385043265-0.30058432164763604j),
               (0.11895422121329963-0.2978596088991513j),
               (0.17564268975687256-0.1467189400154478j),
               (-0.15114188530427297+0.04839289812699797j),
               (-0.14945585920076476-0.18253336396284595j),
               (-0.016980315743620453+0.2201737360468666j),
               (-0.3171953858998003+0.06743388969104153j),
               (-0.03633746314144225+0.2845320656277463j),
               (-0.04871727690995456+0.10055783669361389j),
               (0.15358799192714326+0.30037724866064186j),
               (-0.07364236472525687-0.01732252432300817j),
               (-0.11543828815863978-0.14619702975671972j),
               (-0.08572649254542936+0.004907437124914406j),
               (0.12141014079583456-0.1612580188050374j)],
              [(0.3270998973807755+0.11321132231670365j),
               (-0.23543666040287345+0.0280801649404842j),
               (-0.2059984073903733+0.10599790639877431j),
               (0.050344196452572265-0.09015836283325773j),
               (-0.04065487749133884+0.19826367727289548j),
               (0.13985008692058695-0.27851414101186456j),
               (-0.32770199031193836-0.08665754670680123j),
               (0.15124524973252867-0.4970992821113027j),
               (0.17519935031886236+0.08436702334004455j),
               (0.0432221339203537+0.05737839069253836j),
               (-0.022555674249879597-0.04462756967176236j),
               (0.2185566061307651-0.015594795165700635j),
               (0.10854090654098003-0.013371806001439987j),
               (0.2853935809308845+0.08508059527337587j),
               (0.10352782348171881+0.09544656180446469j),
               (-0.060552416742842216+0.13798242196843136j)],
              [(-0.03669910717478019-0.014837262308440445j),
               (0.07435676443827807-0.021973233759840866j),
               (-0.28724873293576814-0.30744726820543467j),
               (-0.17863013784172135-0.16632683568765746j),
               (0.12375370401182965+0.23363097396159566j),
               (-0.026630516761088078+0.10966504122877428j),
               (-0.01681156337739258-0.2565990924812177j),
               (-0.2065901622037008-0.07220863585141621j),
               (-0.25743736863849426+0.08222426100395705j),
               (-0.05286342877272929-0.025779488154022562j),
               (-0.26407259961243307+0.44054915760385344j),
               (-0.010941215285368452+0.08431679004502719j),
               (0.2639979549168112-0.20177577578930447j),
               (-0.0414519093379409+0.036798688044973396j),
               (-0.2628359697493338-0.009737609020083093j),
               (0.08819246408536309-0.14553971866665452j)],
              [(-0.34301263924483466+0.12025415716812936j),
               (-0.05850925989393835-0.23499882402130223j),
               (-0.1335980584456299-0.02251623571717508j),
               (0.0034386941034220964+0.07287709830411357j),
               (0.2478487364637688-0.22533212262289332j),
               (-0.24483285911483793+0.11599215674508613j),
               (-0.17214462283580945+0.4263893184017798j),
               (0.023066559737535783+0.18035383159184107j),
               (-0.21370881968917155-0.06970684063377065j),
               (-0.030791520486937226-0.14670642772237658j),
               (0.07893356127561806-0.12221823109939256j),
               (0.0512863195135-0.12152117503054423j),
               (0.04057340714526123-0.17375543581591704j),
               (-0.19578826921347156-0.23403268988357j),
               (0.16242236567945123+0.1795232720818837j),
               (-0.2455491074318376-0.006381875989793124j)],
              [(0.10880298766312069+0.14924802820774458j),
               (-0.16343563969556452+0.1754340968170034j),
               (-0.3611764172669411+0.07877302235738501j),
               (-0.04061246509527666+0.03813161816085687j),
               (-0.08015140278900679+0.17483509282411336j),
               (-0.018920452663980687-0.4347337295478453j),
               (-0.36924315514437184-0.13297612178750967j),
               (-0.14860435602837613+0.013908583158505336j),
               (-0.05522175784767437+0.1493492009122914j),
               (-0.10744149457160859+0.12584344993647728j),
               (0.06837268580718867+0.1708845196666436j),
               (-0.06140172948816026-0.07387096374931484j),
               (0.25970300062247387+0.19315814491296904j),
               (-0.0021877113574172435+0.31279112230291034j),
               (-0.09661413401121195+0.04510962035936921j),
               (0.21222105214016374+0.1056160962573064j)],
              [(-0.011163432132399898+0.13895940633986018j),
               (0.17225382849554724-0.053615993962216106j),
               (0.20522533779369925+0.06175625488722937j),
               (0.11498640362750605+0.29553741790363325j),
               (-0.147804335860634-0.09363833405578832j),
               (0.1095896667379122-0.16993272653400868j),
               (-0.046191644770824894+0.21854385710771462j),
               (0.3509659333512959+0.40936590037674914j),
               (-0.06735788972004711+0.22750211075741558j),
               (-0.009629216651023308+0.17733678013548765j),
               (0.08661759255287567+0.34744953756515135j),
               (-0.2899987238302792+0.08271117809691976j),
               (-0.09221179382720593-0.006975513401350697j),
               (0.1955513810356394-0.03436690825554636j),
               (0.1268863398814639-0.041087394039812514j),
               (-0.12856208561849314-0.009001603443587622j)],
              [(0.10691782850772169+0.28143610259983415j),
               (-0.05809986752071057+0.00018377913562662822j),
               (-0.21010991812322083-0.0547645953482295j),
               (0.2795569541163256+0.11886268834715291j),
               (0.01734884394070904-0.01050673503840896j),
               (-0.05753342078649962+0.08596016689112888j),
               (-0.18691215919082227+0.17656949888319257j),
               (-0.21470197435754976-0.07603651975732897j),
               (-0.016808294356419045-0.074815807238821j),
               (-0.14669163338793398+0.10978803265957889j),
               (0.07436468492114505-0.04846259300643488j),
               (0.15001384425905093+0.2459948677939786j),
               (-0.06360458876280331-0.1836461919738599j),
               (0.24930957070284482-0.4275127154371849j),
               (-0.1963698695753302+0.04051916954716545j),
               (-0.2901677604836003-0.3162540299955284j)],
              [(-0.24030628089003736-0.41797616386777314j),
               (-0.150350684138953+0.018326582247807012j),
               (0.0823494713961091+0.06480455093377357j),
               (-0.07131788497025929-0.11077287036228901j),
               (0.026582387987622202-0.0641908649415147j),
               (0.20624886369461148-0.33028714951047966j),
               (0.31798839523245914-0.15523973681357353j),
               (0.03231533387463032-0.0695298657333044j),
               (-0.052389154211624246-0.10050601596162785j),
               (-0.1982760156737719+0.14940852619024855j),
               (0.08269079438280189-0.052880799037700765j),
               (-0.13172764693353434+0.061021121262434946j),
               (-0.10559809465825926-0.051863616371521745j),
               (0.14182599126005518+0.06878961818341074j),
               (0.1500685396571429+0.42970603950890246j),
               (0.15865566271942874+0.2291300503913669j)]]
PROBS_16 = [0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05,
            0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

def make_densop_matrix(vectors, probs):

    dim = len(vectors)
    vectors = np.array(vectors)
    matrix = np.zeros((dim, dim))
    for v,p in zip(vectors, probs):
        matrix = matrix + p * np.outer(v, np.conjugate(v))
    return matrix
    
def make_tenspro_matrices(mat_0, mat_1):

    return np.kron(mat_0, mat_1)

def make_apply_matrix(op, mat):

    matrix = np.dot(mat, np.conjugate(op.T))
    matrix = np.dot(op, matrix)
    return matrix

def add_matrices(mat_0, mat_1):

    return mat_0 + mat_1
    
def mul_matrix(fac, mat):

    return fac * mat
    
def equal_values(val_0, val_1):

    dif = abs(val_0 - val_1)
    if dif < EPS:
        return True
    else:
        return False

def equal_vectors(vec_0, vec_1):

    inpro = abs(np.dot(np.conjugate(vec_0), vec_1))
    if abs(inpro - 1.0) < EPS:
        return True
    else:
        return False

def equal_matrices(mat_0, mat_1):

    vec_0 = mat_0.flatten()
    vec_1 = mat_1.flatten()
    dif = np.linalg.norm(vec_0 - vec_1)
    if dif < EPS:
        return True
    else:
        return False
    
def equal_qstates(qs_0, qs_1):

    fid = qs_0.fidelity(qs_1)
    if abs(fid - 1.0) < EPS:
        return True
    else:
        return False

def equal_densops(de_0, de_1):

    fid = de_0.fidelity(de_1)
    if abs(fid - 1.0) < EPS:
        return True
    else:
        return False

class TestDensOp_init(unittest.TestCase):
    """ test 'DensOp' : '__init__'
    """

    def test_init(self):
        """test '__init__' (qstate, prob)
        """
        dim = 4
        qs = [QState(vector=VECTORS_4[i]) for i in range(dim)]
        pr = PROBS_4
        de = DensOp(qstate=qs, prob=pr)
        actual = de.element
        expect = make_densop_matrix(VECTORS_4, PROBS_4)
        ans = equal_matrices(actual, expect)
        [qs[i].free() for i in range(dim)]
        de.free()
        self.assertEqual(ans,True)

    def test_init_with_matrix(self):
        """test '__init__' (matrix)
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        de = DensOp(matrix=mat)
        actual = de.element
        expect = mat
        ans = equal_matrices(actual, expect)
        de.free()
        self.assertEqual(ans,True)

class TestDensOp_clone(unittest.TestCase):
    """ test 'DensOp' : 'clone'
    """

    def test_clone(self):
        """test 'clone'
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        de = DensOp(matrix=mat)
        de_clone = de.clone()
        actual = de_clone.element
        expect = mat
        ans = equal_matrices(actual, expect)
        de.free()
        de_clone.free()
        self.assertEqual(ans,True)

class TestDensOp_add_mul(unittest.TestCase):
    """ test 'DensOp' : 'add','mul'
    """

    def test_add(self):
        """test 'add'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        de_0 = DensOp(matrix=mat_0)
        de_1 = DensOp(matrix=mat_1)
        de_0.add(de_1)
        actual = de_0.element
        expect = add_matrices(mat_0, mat_1)
        ans = equal_matrices(actual, expect)
        de_0.free()
        de_1.free()
        self.assertEqual(ans,True)

    def test_mul(self):
        """test 'mul'
        """
        fac = 1.0
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        de = DensOp(matrix=mat)
        de.mul(fac)
        actual = de.element
        expect = mul_matrix(fac, mat)
        ans = equal_matrices(actual, expect)
        de.free()
        self.assertEqual(ans,True)

class TestDensOp_trace(unittest.TestCase):
    """ test 'DensOp' : 'trace','sqtrace'
    """

    def test_trace(self):
        """test 'trace'
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        de = DensOp(matrix=mat)
        actual = de.trace()
        expect = 1.0
        ans = equal_values(actual, expect)
        de.free()
        self.assertEqual(ans,True)

    def test_sqtrace(self):
        """test 'sqtrace'
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        de = DensOp(matrix=mat)
        actual = de.sqtrace()
        expect = 0.46978583
        ans = equal_values(actual, expect)
        de.free()
        self.assertEqual(ans,True)

class TestDensOp_composite(unittest.TestCase):
    """ test 'DensOp' : 'patrace','partial','tenspro','composite'
    """

    def test_patrace(self):
        """test 'patrace'
        """
        mat_4 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_2 = make_densop_matrix(VECTORS_2, PROBS_2)
        mat_8 = make_tenspro_matrices(mat_4, mat_2)
        de = DensOp(matrix=mat_8)
        de_pat = de.patrace(id=[0,1])
        actual = de_pat.element
        expect = mat_2
        ans = equal_matrices(actual, expect)
        de.free()
        de_pat.free()
        self.assertEqual(ans,True)

    def test_partial(self):
        """test 'partial'
        """
        mat_4 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_2 = make_densop_matrix(VECTORS_2, PROBS_2)
        mat_8 = make_tenspro_matrices(mat_4, mat_2)
        de = DensOp(matrix=mat_8)
        de_pat = de.partial(id=[2])
        actual = de_pat.element
        expect = mat_2
        ans = equal_matrices(actual, expect)
        de.free()
        de_pat.free()
        self.assertEqual(ans,True)

    def test_tensppro(self):
        """test 'tenspro'
        """
        mat_4 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_2 = make_densop_matrix(VECTORS_2, PROBS_2)
        mat_8 = make_tenspro_matrices(mat_4, mat_2)
        de_4 = DensOp(matrix=mat_4)
        de_2 = DensOp(matrix=mat_2)
        de_8 = de_4.tenspro(de_2)
        actual = de_8.element
        expect = mat_8
        ans = equal_matrices(actual, expect)
        de_4.free()
        de_2.free()
        de_8.free()
        self.assertEqual(ans,True)

    def test_composite(self):
        """test 'compoosite'
        """
        mat_2 = make_densop_matrix(VECTORS_2, PROBS_2)
        mat_4 = make_tenspro_matrices(mat_2, mat_2)
        mat_8 = make_tenspro_matrices(mat_4, mat_2)
        de_2 = DensOp(matrix=mat_2)
        de_8 = de_2.composite(num=3)
        actual = de_8.element
        expect = mat_8
        ans = equal_matrices(actual, expect)
        de_2.free()
        de_8.free()
        self.assertEqual(ans,True)

class TestDensOp_expect(unittest.TestCase):
    """ test 'DensOp' : 'expect'
    """

    def test_expect(self):
        """test 'expect'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        de = DensOp(matrix=mat_0)
        actual = de.expect(matrix=mat_1)
        expect = 0.20425749
        ans = equal_values(actual, expect)
        de.free()
        self.assertEqual(ans,True)

class TestDensOp_apply(unittest.TestCase):
    """ test 'DensOp' : 'apply'
    """

    def test_apply(self):
        """test 'apply'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        de = DensOp(matrix=mat_0)
        de_out = de.apply(matrix=mat_1)
        actual = de.element
        expect = make_apply_matrix(mat_1, mat_0)
        ans = equal_matrices(actual, expect)
        de.free()
        self.assertEqual(ans,True)

class TestDensOp_measurement(unittest.TestCase):
    """ test 'DensOp' : 'probability','instrument'
    """

    inst_res = np.array([[0.80722543+0.j, 0.12486742-0.02537052j],
                         [0.12486742+0.02537052j, 0.19277457+0.j]])
    inst_res_0 = np.array([[0.61445086+0.j, 0.12486742-0.02537052j],
                           [0.12486742+0.02537052j, 0.19277457+0.j]])
    inst_res_1 = np.array([[0.19277457+0.j, 0.+0.j], [0.+0.j, 0.+0.j]])

    def make_povm(self, theta=0.0):

        s = math.sin(theta * math.pi)
        c = math.cos(theta * math.pi)
        f = 1.0/(1.0 + c)
        E0 = f * np.array([[s*s, -c*s], [-c*s, c*c]])
        E1 = f * np.array([[0, 0], [0, 1]])
        E2 = np.eye(2) - E0 - E1
        return (E0, E1, E2)
 
    def make_kraus(self, gamma=0.0):

        transmit = math.sqrt(1.0-gamma)
        reflect = math.sqrt(gamma)
        kraus = []
        kraus.append(np.array([[1,0],[0,0]])+transmit*np.array([[0,0],[0,1]]))
        kraus.append(reflect*np.array([[0,1],[0,0]]))
        return kraus

    def test_probability(self):
        """test 'probability'
        """
        theta = 0.4
        qs = QState(1)
        de = DensOp(qstate=[qs])
        povm = self.make_povm(theta)
        prob = de.probability(povm=povm)
        qs.free()
        de.free()
        self.assertEqual(equal_values(prob[0], 0.69098301), True)
        self.assertEqual(equal_values(prob[1], 0.00000000), True)
        self.assertEqual(equal_values(prob[2], 0.30901699), True)

    def test_instrument(self):
        """test 'instrument' (non-selective)
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        de = DensOp(matrix=mat)
        [M_0,M_1] = self.make_kraus(gamma=0.5)
        de.instrument(kraus=[M_0,M_1])
        actual = de.element
        expect = self.inst_res
        ans = equal_matrices(actual, expect)
        de.free()
        self.assertEqual(ans,True)

    def test_instrument_0(self):
        """test 'instrument' (selective : measured_value=0)
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        de = DensOp(matrix=mat)
        [M_0,M_1] = self.make_kraus(gamma=0.5)
        de.instrument(kraus=[M_0,M_1], measured_value=0)
        actual = de.element
        expect = self.inst_res_0
        ans = equal_matrices(actual, expect)
        de.free()
        self.assertEqual(ans,True)

    def test_instrument_1(self):
        """test 'instrument' (selective : measured_value=1)
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        de = DensOp(matrix=mat)
        [M_0,M_1] = self.make_kraus(gamma=0.5)
        de.instrument(kraus=[M_0,M_1], measured_value=1)
        actual = de.element
        expect = self.inst_res_1
        ans = equal_matrices(actual, expect)
        de.free()
        self.assertEqual(ans,True)

class TestDensOp_similarity(unittest.TestCase):
    """ test 'DensOp' : 'fidelity','distance'
    """

    def test_fidelity(self):
        """test 'fidelity'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        de_0 = DensOp(matrix=mat_0)
        de_1 = DensOp(matrix=mat_1)
        actual = de_0.fidelity(de_1)
        expect = 0.6973384790052483
        ans = equal_values(actual, expect)
        de_0.free()
        de_1.free()
        self.assertEqual(ans,True)
        
    def test_distance(self):
        """test 'fidelity'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        de_0 = DensOp(matrix=mat_0)
        de_1 = DensOp(matrix=mat_1)
        actual = de_0.distance(de_1)
        expect = 0.6395360466162878
        ans = equal_values(actual, expect)
        de_0.free()
        de_1.free()
        self.assertEqual(ans,True)

class TestDensOp_spectrum(unittest.TestCase):
    """ test 'DensOp' : 'spectrum'
    """

    def test_spectrum(self):
        """test 'spectrum'
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        de_0 = DensOp(matrix=mat)
        qstate, prob = de_0.spectrum()
        de_1 = DensOp(qstate=qstate, prob=prob)
        actual = de_0.fidelity(de_1)
        expect = 1.0
        ans = equal_values(actual, expect)
        [q.free() for q in qstate]
        de_0.free()
        de_1.free()
        self.assertEqual(ans,True)

class TestDensOp_entropy(unittest.TestCase):
    """ test 'DensOp' : 'entropy','cond_entropy','mutual_info','relative_entropy'
    """

    def test_entropy_mixed(self):
        """test 'entropy' (for mixed state)
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        de = DensOp(matrix=mat)
        actual = de.entropy()
        expect = 1.3270775661797476
        ans = equal_values(actual, expect)
        de.free()
        self.assertEqual(ans,True)

    def test_entropy_pure(self):
        """test 'entropy' (for sub-systems of pure state)
        """
        qs = QState(vector=VECTORS_4[0])
        de = DensOp(qstate=[qs])
        ent_A = de.entropy(id=[0])
        ent_B = de.entropy(id=[1])
        ans = equal_values(ent_A, ent_B)
        qs.free()
        de.free()
        self.assertEqual(ans,True)

    def test_cond_entropy(self):
        """test 'cond_entropy'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        mat = make_tenspro_matrices(mat_0, mat_1)
        de = DensOp(matrix=mat)
        actual= de.cond_entropy([0,1],[2,3])
        expect = 1.3270774562533503
        ans = equal_values(actual, expect)
        de.free()
        self.assertEqual(ans,True)

    def test_mutual_info(self):
        """test 'mutual_info'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        mat = make_tenspro_matrices(mat_0, mat_1)
        de = DensOp(matrix=mat)
        actual = de.mutual_info([0,1],[2,3])
        expect = 1.0992639731810527e-07
        ans = equal_values(actual, expect)
        de.free()
        self.assertEqual(ans,True)

    def test_relative_entropy(self):
        """test 'relative_entropy'
        """
        mat_0 = make_densop_matrix(VECTORS_4, PROBS_4)
        mat_1 = make_densop_matrix(VECTORS_4_ANOTHER, PROBS_4_ANOTHER)
        de_0 = DensOp(matrix=mat_0)
        de_1 = DensOp(matrix=mat_1)
        actual = de_0.relative_entropy(de_1)
        expect = 2.789437620640274
        ans = equal_values(actual, expect)
        de_0.free()
        de_1.free()
        self.assertEqual(ans,True)

class TestDensOp_1_qubit_gate(unittest.TestCase):
    """ test 'DensOp' : 1-qubit gate
    """

    def test_x(self):
        """test 'x' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).x(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.x(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_y(self):
        """test 'y' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).y(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.y(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_z(self):
        """test 'z' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).z(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.z(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_xr(self):
        """test 'xr' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).xr(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.xr(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_xr_dg(self):
        """test 'xr_dg' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).xr_dg(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.xr_dg(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_h(self):
        """test 'h' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).h(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.h(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_s(self):
        """test 's' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).s(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.s(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_s_dg(self):
        """test 's_dg' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).s_dg(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.s_dg(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_t(self):
        """test 't' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).t(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.t(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_t_dg(self):
        """test 't_dg' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).t_dg(0)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.t_dg(0) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_rx(self):
        """test 'rx' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).rx(0, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.rx(0, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_ry(self):
        """test 'ry' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).ry(0, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.ry(0, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_rz(self):
        """test 'rz' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).rz(0, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.rz(0, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_p(self):
        """test 'p' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).p(0, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.p(0, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_u1(self):
        """test 'u1' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).u1(0, alpha=0.1)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.u1(0, alpha=0.1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_u2(self):
        """test 'u2' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).u2(0, alpha=0.1, beta=0.2)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.u2(0, alpha=0.1, beta=0.2) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_u3(self):
        """test 'u3' gate
        """
        mat = make_densop_matrix(VECTORS_2, PROBS_2)
        actual = DensOp(matrix=mat).u3(0, alpha=0.1, beta=0.2, gamma=0.3)
        qstate = [QState(vector=vec) for vec in VECTORS_2]
        [qs.u3(0, alpha=0.1, beta=0.2, gamma=0.3) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_2)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

class TestDensOp_1_qubit_gate_in_2_reg(unittest.TestCase):
    """ test 'DensOp' : 1-qubit gate in 2-register circuit
    """

    def test_rx_0(self):
        """ test 1-qubit gate in 2-register circuit (reg. #0)
        """
        qid = 0
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).rx(qid, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.rx(qid, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_rx_1(self):
        """ test 1-qubit gate in 2-register circuit (reg. #0)
        """
        qid = 1
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).rx(qid, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.rx(qid, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

class TestQState_2_qubit(unittest.TestCase):
    """ test 'QState' : 2-qubit gate
    """

    def test_cx(self):
        """test 'cx' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cx(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cx(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cy(self):
        """test 'cy' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cy(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cy(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cz(self):
        """test 'cz' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cz(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cz(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cxr(self):
        """test 'cxr' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cxr(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cxr(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cxr_dg(self):
        """test 'cxr_dg' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cxr_dg(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cxr_dg(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_ch(self):
        """test 'ch' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).ch(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.ch(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cs(self):
        """test 'cs' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cs(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cs(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)
        
    def test_cs_dg(self):
        """test 'cs_dg' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cs_dg(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cs_dg(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_ct(self):
        """test 'ct' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).ct(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.ct(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_ct_dg(self):
        """test 'ct_dg' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).ct_dg(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.ct_dg(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_sw(self):
        """test 'sw' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).sw(0,1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.sw(0,1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_crx(self):
        """test 'crx' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).crx(0,1, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.crx(0,1, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cry(self):
        """test 'cry' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cry(0,1, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cry(0,1, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_crz(self):
        """test 'crz' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).crz(0,1, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.crz(0,1, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cp(self):
        """test 'cp'gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cp(0,1, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cp(0,1, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cu1(self):
        """test 'cu1' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cu1(0,1, alpha=0.1)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cu1(0,1, alpha=0.1) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cu2(self):
        """test 'cu2' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cu2(0,1, alpha=0.1, beta=0.2)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cu2(0,1, alpha=0.1, beta=0.2) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_cu3(self):
        """test 'cu3' gate
        """
        mat = make_densop_matrix(VECTORS_4, PROBS_4)
        actual = DensOp(matrix=mat).cu3(0,1, alpha=0.1, beta=0.2, gamma=0.3)
        qstate = [QState(vector=vec) for vec in VECTORS_4]
        [qs.cu3(0,1, alpha=0.1, beta=0.2, gamma=0.3) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_4)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

class TestDensOp_2_qubit_in_3_reg(unittest.TestCase):
    """ test 'DensOp' : 2-qubit gate in 3-register circuit
    """

    def test_crx_0_1(self):
        """ test 2-qubit gate in 3-register circuit (reg. #0,#1)
        """
        mat = make_densop_matrix(VECTORS_8, PROBS_8)
        actual = DensOp(matrix=mat).crx(0,1, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_8]
        [qs.crx(0,1, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_8)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_crx_1_2(self):
        """ test 2-qubit gate in 3-register circuit (reg. #1,#2)
        """
        mat = make_densop_matrix(VECTORS_8, PROBS_8)
        actual = DensOp(matrix=mat).crx(1,2, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_8]
        [qs.crx(1,2, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_8)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_crx_2_0(self):
        """ test 2-qubit gate in 3-register circuit (reg. #2,#0)
        """
        mat = make_densop_matrix(VECTORS_8, PROBS_8)
        actual = DensOp(matrix=mat).crx(2,0, phase=0.25)
        qstate = [QState(vector=vec) for vec in VECTORS_8]
        [qs.crx(2,0, phase=0.25) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_8)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)
        
class TestDensOp_3_qubit(unittest.TestCase):
    """ test 'DensOp' : 3-qubit gate
    """

    def test_ccx(self):
        """test 'ccx' gate
        """
        mat = make_densop_matrix(VECTORS_8, PROBS_8)
        actual = DensOp(matrix=mat).ccx(0,1,2)
        qstate = [QState(vector=vec) for vec in VECTORS_8]
        [qs.ccx(0,1,2) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_8)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_csw(self):
        """test 'csw' gate
        """
        mat = make_densop_matrix(VECTORS_8, PROBS_8)
        actual = DensOp(matrix=mat).csw(0,1,2)
        qstate = [QState(vector=vec) for vec in VECTORS_8]
        [qs.csw(0,1,2) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_8)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

class TestQState_n_qubit(unittest.TestCase):
    """ test 'QState' : n-qubit gate
    """

    def test_mcx_3(self):
        """test 'mcx' gate (3-qubit)
        """
        mat = make_densop_matrix(VECTORS_8, PROBS_8)
        actual = DensOp(matrix=mat).mcx(id=[0,1,2])
        qstate = [QState(vector=vec) for vec in VECTORS_8]
        [qs.mcx(id=[0,1,2]) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_8)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

    def test_mcx_4(self):
        """test 'mcx' gate (4-qubit)
        """
        mat = make_densop_matrix(VECTORS_16, PROBS_16)
        actual = DensOp(matrix=mat).mcx(id=[0,1,2,3])
        qstate = [QState(vector=vec) for vec in VECTORS_16]
        [qs.mcx(id=[0,1,2,3]) for qs in qstate]
        expect = DensOp(qstate=qstate, prob=PROBS_16)
        ans = equal_densops(actual, expect)
        [qs.free() for qs in qstate]
        actual.free()
        expect.free()
        self.assertEqual(ans,True)

if __name__ == '__main__':
    unittest.main()
