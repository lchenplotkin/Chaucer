import re
import string

# Function to break a word into syllables, considering vowel combinations and consonant blends
vowels = "aeiouy"
def break_into_syllables(word):
    vowels = "aeiouy"
    
    # Treat combinations as single syllables (vowel combinations and consonant blends)
    word = word.lower()
    
    # Replace common vowel combinations with placeholders to treat them as single syllables
    word = word.replace("ou", "ou_")  # Treat "ou" as a single syllable unit (e.g., flour)
    word = word.replace("ai", "ai_")  # Treat "ai" as a single syllable unit
    word = word.replace("ei", "ei_")  # Treat "ei" as a single syllable unit
    word = word.replace("au", "au_")  # Treat "au" as a single syllable unit
    word = word.replace("ea", "ea_")  # Treat "ea" as a single syllable unit (e.g., "bread")
    word = word.replace("ie", "ie_")  # Treat "ie" as a single syllable unit
    word = word.replace("oo", "oo_")  # Treat "oo" as a single syllable unit
    
    # Consonant blends that should be treated as part of the syllable
    word = word.replace("sh", "sh_")  # Treat "sh" as a single unit
    word = word.replace("ch", "ch_")  # Treat "ch" as a single unit
    word = word.replace("st", "st_")  # Treat "st" as a single unit
    word = word.replace("cl", "cl_")  # Treat "cl" as a single unit
    word = word.replace("fl", "fl_")  # Treat "fl" as a single unit
    word = word.replace("gl", "gl_")  # Treat "gl" as a single unit
    word = word.replace("bl", "bl_")  # Treat "bl" as a single unit
    word = word.replace("wh", "wh_")  # Treat "wh" as a single unit
    word = word.replace("gh", "gh_")  # Treat "gh" as a single unit
    word = word.replace("th", "th_")  # Treat "th" as a single unit
    
    # Now split based on vowels and consonant clusters
    syllables = re.findall(r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*|$)', word)
    
    # Replace the placeholders back to their original form
    syllables = [syllable.replace("ou_", "ou").replace("ai_", "ai").replace("ei_", "ei")
                 .replace("au_", "au").replace("ea_", "ea").replace("ie_", "ie")
                 .replace("oo_", "oo").replace("sh_", "sh").replace("ch_", "ch")
                 .replace("st_", "st").replace("cl_", "cl").replace("fl_", "fl")
                 .replace("gl_", "gl").replace("bl_", "bl").replace("wh_", "wh")
                 .replace("gh_", "gh").replace("th_", "th") for syllable in syllables]

    print(syllables)
    
    return syllables

# Function to check the rhyme type (masculine or feminine)
def get_rhyme_type(word1, word2):
    syllables1 = break_into_syllables(word1)
    syllables2 = break_into_syllables(word2)

    if len(syllables1) == 1 or len(syllables2) == 1:
        return "M"
    
    last_syllable1 = syllables1[-1]
    last_syllable2 = syllables2[-1]

    
    if last_syllable1 == last_syllable2:
        # For feminine rhyme, there should be an additional matching syllable before the last one
        if len(syllables1) > 1 and len(syllables2) > 1:
            syllables1 = syllables1[:-1]
            syllables2 = syllables2[:-1]
            if last_syllable1 == "e" and last_syllable2 == "e" and len(syllables1) > 1 and len(syllables2) >1:
                syllables1 = syllables1[:-1]
                syllables2 = syllables2[:-1]
            if syllables1[-1] == syllables2[-1]:
                return "F"
            elif last_syllable1!="e" and set(syllables1[-1]).intersection(set(vowels)) == set(syllables2[-1]).intersection(set(vowels)):
                user = input(f"{word1},{word2},{syllables1},{syllables2}")
                return user
            else:
                return "M"
        else:
            return "M"
    else:
        user = input(f"{word1},{word2},{syllables1},{syllables2}")
        return user
    return "No Rhyme"

    return "WHAT"
# Function to extract the final words of each line in the text, removing punctuation
lines = []
def get_final_words(text):
    global lines
    lines = text.split('\n')
    final_words = []
    for line in lines:
        line = line.strip()
        if line:  # Only process non-empty lines
            words = line.split()
            # Remove punctuation from the final word
            final_word = words[-1].strip(string.punctuation)
            final_words.append(final_word)  # Add the cleaned word to the list
    return final_words

# Example text (Middle English from The Canterbury Tales)
text = """
Whan that Aprille with his shoures soote,
The droghte of March hath perced to the roote,
And bathed every veyne in swich licóur
Of which vertú engendred is the flour;
Whan Zephirus eek with his swete breeth
Inspired hath in every holt and heeth
The tendre croppes, and the yonge sonne
Hath in the Ram his halfe cours y-ronne,
And smale foweles maken melodye,
That slepen al the nyght with open ye,
So priketh hem Natúre in hir corages,
Thanne longen folk to goon on pilgrimages,
And palmeres for to seken straunge strondes,
To ferne halwes, kowthe in sondry londes;
And specially, from every shires ende
Of Engelond, to Caunterbury they wende,
The hooly blisful martir for to seke,
That hem hath holpen whan that they were seeke.

Bifil that in that seson on a day,
In Southwerk at the Tabard as I lay,
Redy to wenden on my pilgrymage
To Caunterbury with ful devout corage,
At nyght were come into that hostelrye
Wel nyne and twenty in a compaignye
Of sondry folk, by áventure y-falle
In felaweshipe, and pilgrimes were they alle,
That toward Caunterbury wolden ryde.
The chambres and the stables weren wyde,
And wel we weren esed atte beste.
And shortly, whan the sonne was to reste,
So hadde I spoken with hem everychon,
That I was of hir felaweshipe anon,
And made forward erly for to ryse,
To take oure wey, ther as I yow devyse.

But nathelees, whil I have tyme and space,
Er that I ferther in this tale pace,
Me thynketh it acordaunt to resoun
To telle yow al the condicioun
Of ech of hem, so as it semed me,
And whiche they weren and of what degree,
And eek in what array that they were inne;
And at a Knyght than wol I first bigynne.

A Knyght ther was, and that a worthy man,
That fro the tyme that he first bigan
To riden out, he loved chivalrie,
Trouthe and honóur, fredom and curteisie.
Ful worthy was he in his lordes werre,
And thereto hadde he riden, no man ferre,
As wel in cristendom as in hethenesse,
And evere honóured for his worthynesse.
At Alisaundre he was whan it was wonne;
Ful ofte tyme he hadde the bord bigonne
Aboven alle nacions in Pruce.
In Lettow hadde he reysed and in Ruce,—
No cristen man so ofte of his degree.
In Gernade at the seege eek hadde he be
Of Algezir, and riden in Belmarye.
At Lyeys was he, and at Satalye,
Whan they were wonne; and in the Grete See
At many a noble armee hadde he be.

At mortal batailles hadde he been fiftene,
And foughten for oure feith at Tramyssene
In lyste thries, and ay slayn his foo.
This ilke worthy knyght hadde been also
Somtyme with the lord of Palatye
Agayn another hethen in Turkye;
And evermoore he hadde a sovereyn prys.
And though that he were worthy, he was wys,
And of his port as meeke as is a mayde.
He nevere yet no vileynye ne sayde,
In al his lyf, unto no maner wight.
He was a verray, parfit, gentil knyght.

But for to tellen yow of his array,
His hors weren goode, but he was nat gay;
Of fustian he wered a gypon
Al bismótered with his habergeon;
For he was late y-come from his viage,
And wente for to doon his pilgrymage.

With hym ther was his sone, a yong Squiér,
A lovyere and a lusty bacheler,
With lokkes crulle as they were leyd in presse.
Of twenty yeer of age he was, I gesse.
Of his statúre he was of evene lengthe,
And wonderly delyvere and of greet strengthe.
And he hadde been somtyme in chyvachie
In Flaundres, in Artoys, and Pycardie,
And born hym weel, as of so litel space,
In hope to stonden in his lady grace.
Embrouded was he, as it were a meede
Al ful of fresshe floures whyte and reede.
Syngynge he was, or floytynge, al the day;
He was as fressh as is the month of May.
Short was his gowne, with sleves longe and wyde;
Wel koude he sitte on hors and faire ryde;
He koude songes make and wel endite,
Juste and eek daunce, and weel purtreye and write.
So hoote he lovede that by nyghtertale
He sleep namoore than dooth a nyghtyngale.
Curteis he was, lowely and servysáble,
And carf biforn his fader at the table.

A Yeman hadde he and servántz namo
At that tyme, for hym liste ride soo;
And he was clad in cote and hood of grene.
A sheef of pecock arwes bright and kene,
Under his belt he bar ful thriftily—
Wel koude he dresse his takel yemanly;
His arwes drouped noght with fetheres lowe—
And in his hand he baar a myghty bowe.
A not-heed hadde he, with a broun viságe.
Of woodecraft wel koude he al the uságe.
Upon his arm he baar a gay bracér,
And by his syde a swerd and a bokeler,
And on that oother syde a gay daggere,
Harneised wel and sharp as point of spere;
A Cristophere on his brest of silver sheene.
An horn he bar, the bawdryk was of grene.
A forster was he, soothly as I gesse.

Ther was also a Nonne, a Prioresse,
That of hir smylyng was ful symple and coy;
Hire gretteste ooth was but by seinte Loy,
And she was cleped madame Eglentyne.
Ful weel she soong the service dyvyne,
Entuned in hir nose ful semely;
And Frenssh she spak ful faire and fetisly,
After the scole of Stratford atte Bowe,
For Frenssh of Parys was to hire unknowe.
At mete wel y-taught was she with-alle:
She leet no morsel from hir lippes falle,
Ne wette hir fyngres in hir sauce depe.
Wel koude she carie a morsel and wel kepe
Thát no drope ne fille upon hire brist;
In curteisie was set ful muchel hir list.
Hire over-lippe wyped she so clene
That in hir coppe ther was no ferthyng sene
Of grece, whan she dronken hadde hir draughte.
Ful semely after hir mete she raughte.
And sikerly she was of greet desport,
And ful plesáunt and amyable of port,
And peyned hire to countrefete cheere
Of court, and been estatlich of manere,
And to ben holden digne of reverence.
But for to speken of hire conscience,
She was so charitable and so pitous
She wolde wepe if that she saugh a mous
Kaught in a trappe, if it were deed or bledde.
Of smale houndes hadde she, that she fedde
With rosted flessh, or milk and wastel breed;
But soore wepte she if oon of hem were deed,
Or if men smoot it with a yerde smerte;
And al was conscience and tendre herte.

Ful semyly hir wympul pynched was;
Hire nose tretys, her eyen greye as glas,
Hir mouth ful smal and ther-to softe and reed;
But sikerly she hadde a fair forheed;
It was almoost a spanne brood, I trowe;
For, hardily, she was nat undergrowe.
Ful fetys was hir cloke, as I was war;
Of smal coral aboute hire arm she bar
A peire of bedes, gauded al with grene,
And ther-on heng a brooch of gold ful sheene,
On which ther was first write a crowned A,
And after, Amor vincit omnia.

Another Nonne with hire hadde she,
That was hire chapeleyne, and Preestes thre.

A Monk ther was, a fair for the maistrie,
An outridere, that lovede venerie;
A manly man, to been an abbot able.
Ful many a deyntee hors hadde he in stable;
And whan he rood, men myghte his brydel heere
Gýnglen in a whistlynge wynd als cleere,
And eek as loude, as dooth the chapel belle,
Ther as this lord was kepere of the celle.
The reule of seint Maure or of seint Beneit,
By-cause that it was old and som-del streit,—
This ilke Monk leet olde thynges pace,
And heeld after the newe world the space.
He yaf nat of that text a pulled hen
That seith that hunters ben nat hooly men,
Ne that a monk, whan he is recchelees,
Is likned til a fissh that is waterlees,—
This is to seyn, a monk out of his cloystre.
But thilke text heeld he nat worth an oystre;
And I seyde his opinioun was good.
What sholde he studie and make hymselven wood,
Upon a book in cloystre alwey to poure,
Or swynken with his handes and labóure,
As Austyn bit? How shal the world be served?
Lat Austyn have his swynk to him reserved.
Therfore he was a prikasour aright:
Grehoundes he hadde, as swift as fowel in flight;
Of prikyng and of huntyng for the hare
Was al his lust, for no cost wolde he spare.
I seigh his sleves y-púrfiled at the hond
With grys, and that the fyneste of a lond;
And for to festne his hood under his chyn
He hadde of gold y-wroght a curious pyn;
A love-knotte in the gretter ende ther was.
His heed was balled, that shoon as any glas,
And eek his face, as he hadde been enoynt.
He was a lord ful fat and in good poynt;
His eyen stepe, and rollynge in his heed,
That stemed as a forneys of a leed;
His bootes souple, his hors in greet estaat.
Now certeinly he was a fair prelaat.
He was nat pale, as a forpyned goost:
A fat swan loved he best of any roost.
His palfrey was as broun as is a berye.

A Frere ther was, a wantowne and a merye,
A lymytour, a ful solémpne man.
In alle the ordres foure is noon that kan
So muchel of daliaunce and fair langage.
He hadde maad ful many a mariage
Of yonge wommen at his owene cost.
Unto his ordre he was a noble post.
Ful wel biloved and famulier was he
With frankeleyns over al in his contree,
And eek with worthy wommen of the toun;
For he hadde power of confessioun,
As seyde hym-self, moore than a curát,
For of his ordre he was licenciat.
Ful swetely herde he confessioun,
And plesaunt was his absolucioun.
He was an esy man to yeve penaunce
There as he wiste to have a good pitaunce;
For unto a povre ordre for to yive
Is signe that a man is wel y-shryve;
For, if he yaf, he dorste make avaunt
He wiste that a man was répentaunt;
For many a man so hard is of his herte
He may nat wepe al-thogh hym soore smerte.
Therfore in stede of wepynge and preyéres
Men moote yeve silver to the povre freres.
His typet was ay farsed full of knyves
And pynnes, for to yeven faire wyves.
And certeinly he hadde a murye note:
Wel koude he synge and pleyen on a rote;
Of yeddynges he baar outrely the pris.
His nekke whit was as the flour-de-lys;
Ther-to he strong was as a champioun.
He knew the tavernes wel in every toun,
And everich hostiler and tappestere
Bet than a lazar or a beggestere;
For unto swich a worthy man as he
Acorded nat, as by his facultee,
To have with sike lazars aqueyntaunce;
It is nat honest, it may nat avaunce
Fór to deelen with no swich poraille,
But al with riche and selleres of vitaille.
And over-al, ther as profit sholde arise,
Curteis he was and lowely of servyse.
Ther nas no man nowher so vertuous.
He was the beste beggere in his hous;
[And yaf a certeyn ferme for the graunt,
Noon of his brethren cam ther in his haunt;]
For thogh a wydwe hadde noght a sho,
So plesaunt was his In principio,
Yet wolde he have a ferthyng er he wente:
His purchas was wel bettre than his rente.
And rage he koude, as it were right a whelpe.
In love-dayes ther koude he muchel helpe,
For there he was nat lyk a cloysterer
With a thredbare cope, as is a povre scolér,
But he was lyk a maister, or a pope;
Of double worstede was his semycope,
That rounded as a belle, out of the presse.
Somwhat he lipsed for his wantownesse,
To make his Englissh sweete upon his tonge;
And in his harpyng, whan that he hadde songe,
His eyen twynkled in his heed aryght
As doon the sterres in the frosty nyght.
This worthy lymytour was cleped Hubérd.

A Marchant was ther with a forked berd,
In motteleye, and hye on horse he sat;
Upon his heed a Flaundryssh bevere hat;
His bootes clasped faire and fetisly.
His resons he spak ful solémpnely,
Sownynge alway thencrees of his wynnyng.
He wolde the see were kept for any thing
Bitwixe Middelburgh and Orewelle.
Wel koude he in eschaunge sheeldes selle.
This worthy man ful wel his wit bisette;
Ther wiste no wight that he was in dette,
So estatly was he of his gouvernaunce,
With his bargaynes and with his chevyssaunce.
For sothe he was a worthy man with-alle,
But, sooth to seyn, I noot how men hym calle.

A Clerk ther was of Oxenford also,
That unto logyk hadde longe y-go.
As leene was his hors as is a rake,
And he nas nat right fat, I undertake,
But looked holwe, and ther-to sobrely.
Ful thredbare was his overeste courtepy;
For he hadde geten hym yet no benefice,
Ne was so worldly for to have office;
For hym was lévere háve at his beddes heed
Twénty bookes, clad in blak or reed,
Of Aristotle and his philosophie,
Than robes riche, or fíthele, or gay sautrie.
But al be that he was a philosophre,
Yet hadde he but litel gold in cofre;
But al that he myghte of his freendes hente
On bookes and on lernynge he it spente,
And bisily gan for the soules preye
Of hem that yaf hym wher-with to scoleye.
Of studie took he moost cure and moost heede.
Noght o word spak he moore than was neede;
And that was seyd in forme and reverence,
And short and quyk and ful of hy senténce.
Sownynge in moral vertu was his speche;
And gladly wolde he lerne and gladly teche.

A Sergeant of the Lawe, war and wys,
That often hadde been at the Parvys,
Ther was also, ful riche of excellence.
Discreet he was, and of greet reverence—
He semed swich, his wordes weren so wise.
Justice he was ful often in assise,
By patente, and by pleyn commissioun.
For his science and for his heigh renoun,
Of fees and robes hadde he many oon.
So greet a purchasour was nowher noon:
Al was fee symple to hym in effect;
His purchasyng myghte nat been infect.
Nowher so bisy a man as he ther nas,
And yet he semed bisier than he was.
In termes hadde he caas and doomes alle
That from the tyme of kyng William were falle.
Ther-to he koude endite and make a thyng,
Ther koude no wight pynche at his writyng;
And every statut koude he pleyn by rote.
He rood but hoomly in a medlee cote,
Girt with a ceint of silk, with barres smale;
Of his array telle I no lenger tale.

A Frankeleyn was in his compaignye.
Whit was his berd as is the dayesye;
Of his complexioun he was sangwyn.
Wel loved he by the morwe a sop in wyn;
To lyven in delit was evere his wone,
For he was Epicurus owene sone,
That heeld opinioun that pleyn delit
Was verraily felicitee parfit.
An housholdere, and that a greet, was he;
Seint Julian he was in his contree.
His breed, his ale, was alweys after oon;
A bettre envyned man was nowher noon.
Withoute bake mete was nevere his hous,
Of fissh and flessh, and that so plentevous,
It snewed in his hous of mete and drynke,
Of alle deyntees that men koude thynke,
After the sondry sesons of the yeer;
So chaunged he his mete and his soper.
Ful many a fat partrich hadde he in muwe,
And many a breem and many a luce in stuwe.
Wo was his cook but if his sauce were
Poynaunt and sharp, and redy al his geere.
His table dormant in his halle alway
Stood redy covered al the longe day.
At sessiouns ther was he lord and sire;
Ful ofte tyme he was knyght of the shire.
An anlaas, and a gipser al of silk,
Heeng at his girdel, whit as morne milk.
A shirreve hadde he been, and a countour;
Was nowher such a worthy vavasour.

An Haberdasshere, and a Carpenter,
A Webbe, a Dyere, and a Tapycer,—
And they were clothed alle in o lyveree
Of a solémpne and a greet fraternitee.
Ful fressh and newe hir geere apiked was;
Hir knyves were chaped noght with bras,
But al with silver; wroght ful clene and weel
Hire girdles and hir pouches everydeel.
Wel semed ech of hem a fair burgeys
To sitten in a yeldehalle, on a deys.
Éverich, for the wisdom that he kan,
Was shaply for to been an alderman;
For catel hadde they ynogh and rente,
And eek hir wyves wolde it wel assente,
And elles certeyn were they to blame.
It is ful fair to been y-cleped Madame,
And goon to vigilies al bifore,
And have a mantel roialliche y-bore.

A Cook they hadde with hem for the nones,
To boille the chiknes with the marybones,
And poudre-marchant tart, and galyngale.
Wel koude he knowe a draughte of Londoun ale.
He koude rooste, and sethe, and broille, and frye,
Máken mortreux, and wel bake a pye.
But greet harm was it, as it thoughte me,
That on his shyne a mormal hadde he;
For blankmanger, that made he with the beste.

A Shipman was ther, wonynge fer by weste;
For aught I woot he was of Dertemouthe.
He rood upon a rouncy, as he kouthe,
In a gowne of faldyng to the knee.
A daggere hangynge on a laas hadde he
Aboute his nekke, under his arm adoun.
The hoote somer hadde maad his hewe al broun;
And certeinly he was a good felawe.
Ful many a draughte of wyn hadde he y-drawe
Fro Burdeux-ward, whil that the chapman sleep.
Of nyce conscience took he no keep.
If that he faught and hadde the hyer hond,
By water he sente hem hoom to every lond.
But of his craft to rekene wel his tydes,
His stremes, and his daungers hym bisides,
His herberwe and his moone, his lode-menage,
Ther nas noon swich from Hulle to Cartage.
Hardy he was and wys to undertake;
With many a tempest hadde his berd been shake.
He knew alle the havenes, as they were,
From Gootlond to the Cape of Fynystere,
And every cryke in Britaigne and in Spayne.
His barge y-cleped was the Maudelayne.

With us ther was a Doctour of Phisik;
In all this world ne was ther noon hym lik,
To speke of phisik and of surgerye;
For he was grounded in astronomye.
He kepte his pacient a ful greet deel
In houres, by his magyk natureel.
Wel koude he fortunen the ascendent
Of his ymáges for his pacient.
He knew the cause of everich maladye,
Were it of hoot, or cold, or moyste, or drye,
And where they engendred and of what humour.
He was a verray, parfit praktisour;
The cause y-knowe, and of his harm the roote,
Anon he yaf the sike man his boote.
Ful redy hadde he his apothecaries
To sende him drogges and his letuaries;
For ech of hem made oother for to wynne,
Hir frendshipe nas nat newe to bigynne.
Wel knew he the olde Esculapius,
And De{"y}scorides, and eek Rufus,
Old Ypocras, Haly, and Galyen,
Serapion, Razis, and Avycen,
Averrois, Damascien, and Constantyn,
Bernard, and Gatesden, and Gilbertyn.
Of his diete mesurable was he,
For it was of no superfluitee,
But of greet norissyng and digestíble.
His studie was but litel on the Bible.
In sangwyn and in pers he clad was al,
Lyned with taffata and with sendal.
And yet he was but esy of dispence;
He kepte that he wan in pestilence.
For gold in phisik is a cordial;
Therfore he lovede gold in special.

A Good Wif was ther of biside Bathe,
But she was som-del deef, and that was scathe.
Of clooth-makyng she hadde swich an haunt
She passed hem of Ypres and of Gaunt.
In al the parisshe wif ne was ther noon
That to the offrynge bifore hire sholde goon;
And if ther dide, certeyn so wrooth was she
That she was out of alle charitee.
Hir coverchiefs ful fyne weren of ground;
I dorste swere they weyeden ten pound
That on a Sonday weren upon hir heed.
Hir hosen weren of fyn scarlet reed,
Ful streite y-teyd, and shoes ful moyste and newe.
Boold was hir face, and fair, and reed of hewe.
She was a worthy womman al hir lyve;
Housbondes at chirche dore she hadde fyve,
Withouten oother compaignye in youthe;
But ther-of nedeth nat to speke as nowthe.
And thries hadde she been at Jérusalem;
She hadde passed many a straunge strem;
At Rome she hadde been, and at Boloigne,
In Galice at Seint Jame, and at Coloigne.
She koude muchel of wandrynge by the weye.
Gat-tothed was she, soothly for to seye.
Upon an amblere esily she sat,
Y-wympled wel, and on hir heed an hat
As brood as is a bokeler or a targe;
A foot-mantel aboute hir hipes large,
And on hire feet a paire of spores sharpe.
In felaweshipe wel koude she laughe and carpe;
Of remedies of love she knew per chauncé,
For she koude of that art the olde daunce.

A good man was ther of religioun,
And was a povre Person of a Toun;
But riche he was of hooly thoght and werk.
He was also a lerned man, a clerk,
That Cristes Gospel trewely wolde preche;
His parisshens devoutly wolde he teche.
Benygne he was, and wonder diligent,
And in adversitee ful pacient;
And swich he was y-preved ofte sithes.
Ful looth were hym to cursen for his tithes,
But rather wolde he yeven, out of doute,
Unto his povre parisshens aboute,
Of his offrýng and eek of his substaunce;
He koude in litel thyng have suffisaunce.
Wyd was his parisshe, and houses fer asonder,
But he ne lafte nat, for reyn ne thonder,
In siknesse nor in meschief to visíte
The ferreste in his parisshe, muche and lite,
Upon his feet, and in his hand a staf.
This noble ensample to his sheep he yaf,
That first he wroghte and afterward he taughte.
Out of the gospel he tho wordes caughte;
And this figure he added eek therto,
That if gold ruste, what shal iren doo?
For if a preest be foul, on whom we truste,
No wonder is a lewed man to ruste;
And shame it is, if a prest take keep,
A shiten shepherde and a clene sheep.
Wel oghte a preest ensample for to yive
By his clennesse how that his sheep sholde lyve.
He sette nat his benefice to hyre
And leet his sheep encombred in the myre,
And ran to Londoun, unto Seinte Poules,
To seken hym a chaunterie for soules,
Or with a bretherhed to been withholde;
But dwelte at hoom and kepte wel his folde,
So that the wolf ne made it nat myscarie;
He was a shepherde, and noght a mercenarie.
And though he hooly were and vertuous,
He was to synful man nat despitous,
Ne of his speche daungerous ne digne,
But in his techyng díscreet and benygne.
To drawen folk to hevene by fairnesse,
By good ensample, this was his bisynesse.
But it were any persone obstinat,
What so he were, of heigh or lough estat,
Hym wolde he snybben sharply for the nonys.
A bettre preest I trowe that nowher noon ys.
He waited after no pompe and reverence,
Ne maked him a spiced conscience;
But Cristes loore and his apostles twelve
He taughte, but first he folwed it hymselve.

With hym ther was a Plowman, was his brother,
That hadde y-lad of dong ful many a fother;
A trewe swynkere and a good was he,
Lyvynge in pees and parfit charitee.
God loved he best, with al his hoole herte,
At alle tymes, thogh him gamed or smerte.
And thanne his neighebor right as hymselve.
He wolde thresshe, and therto dyke and delve,
For Cristes sake, for every povre wight,
Withouten hire, if it lay in his myght.
His tithes payede he ful faire and wel,
Bothe of his propre swynk and his catel.
In a tabard he rood upon a mere.

Ther was also a Reve and a Millere,
A Somnour and a Pardoner also,
A Maunciple, and myself,—ther were namo.

The Millere was a stout carl for the nones;
Ful byg he was of brawn and eek of bones.
That proved wel, for over-al, ther he cam,
At wrastlynge he wolde have alwey the ram.
He was short-sholdred, brood, a thikke knarre;
Ther nas no dore that he nolde heve of harre,
Or breke it at a rennyng with his heed.
His berd as any sowe or fox was reed,
And therto brood, as though it were a spade.
Upon the cop right of his nose he hade
A werte, and thereon stood a toft of herys,
Reed as the brustles of a sowes erys;
His nosethirles blake were and wyde.
A swerd and a bokeler bar he by his syde.
His mouth as greet was as a greet forneys;
He was a janglere and a goliardeys,
And that was moost of synne and harlotries.
Wel koude he stelen corn and tollen thries;
And yet he hadde a thombe of gold, pardee.
A whit cote and a blew hood wered he.
A baggepipe wel koude he blowe and sowne,
And therwithal he broghte us out of towne.

A gentil Maunciple was ther of a temple,
Of which achátours myghte take exemple
For to be wise in byynge of vitaille;
For, wheither that he payde or took by taille,
Algate he wayted so in his achaat
That he was ay biforn and in good staat.
Now is nat that of God a ful fair grace,
That swich a lewed mannes wit shal pace
The wisdom of an heep of lerned men?
Of maistres hadde he mo than thries ten,
That weren of lawe expert and curious,
Of whiche ther weren a duszeyne in that hous
Worthy to been stywardes of rente and lond
Of any lord that is in Engelond,
To maken hym lyve by his propre good,
In honour dettelees, but if he were wood,
Or lyve as scarsly as hym list desire;
And able for to helpen al a shire
In any caas that myghte falle or happe;
And yet this Manciple sette hir aller cappe

The Reve was a sclendre colerik man.
His berd was shave as ny as ever he kan;
His heer was by his erys round y-shorn;
His top was dokked lyk a preest biforn.
Ful longe were his legges and ful lene,
Y-lyk a staf, ther was no calf y-sene.
Wel koude he kepe a gerner and a bynne;
Ther was noon auditour koude on him wynne.
Wel wiste he, by the droghte and by the reyn,
The yeldynge of his seed and of his greyn.
His lordes sheep, his neet, his dayerye,
His swyn, his hors, his stoor, and his pultrye,
Was hoolly in this reves governyng;
And by his covenant yaf the rekenyng
Syn that his lord was twenty yeer of age;
There koude no man brynge hym in arrerage.
There nas baillif, ne hierde, nor oother hyne,
That he ne knew his sleighte and his covyne;
They were adrad of hym as of the deeth.
His wonyng was ful fair upon an heeth;
With grene trees shadwed was his place.
He koude bettre than his lord purchace;
Ful riche he was a-stored pryvely.
His lord wel koude he plesen subtilly,
To yeve and lene hym of his owene good,
And have a thank, and yet a cote and hood.
In youthe he hadde lerned a good myster;
He was a wel good wrighte, a carpenter.
This Reve sat upon a ful good stot,
That was al pomely grey, and highte Scot.
A long surcote of pers upon he hade,
And by his syde he baar a rusty blade.
Of Northfolk was this Reve of which I telle,
Biside a toun men clepen Baldeswelle.
Tukked he was as is a frere, aboute.
And evere he rood the hyndreste of oure route.

A Somonour was ther with us in that place,
That hadde a fyr-reed cherubynnes face,
For sawcefleem he was, with eyen narwe.
As hoot he was and lecherous as a sparwe,
With scaled browes blake and piled berd,—
Of his visage children were aferd.
Ther nas quyk-silver, lytarge, ne brymstoon,
Boras, ceruce, ne oille of tartre noon,
Ne oynement that wolde clense and byte,
That hym myghte helpen of his whelkes white,
Nor of the knobbes sittynge on his chekes.
Wel loved he garleek, oynons, and eek lekes,
And for to drynken strong wyn, reed as blood.
Thanne wolde he speke, and crie as he were wood.
And whan that he wel dronken hadde the wyn,
Than wolde he speke no word but Latyn.
A fewe termes hadde he, two or thre,
That he had lerned out of som decree,—
No wonder is, he herde it al the day;
And eek ye knowen wel how that a jay
Kan clepen "Watte" as wel as kan the pope.
But whoso koude in oother thyng hym grope,
Thanne hadde he spent al his philosophie;
Ay "Questio quid juris" wolde he crie.
He was a gentil harlot and a kynde;
A bettre felawe sholde men noght fynde.
He wolde suffre for a quart of wyn
A good felawe to have his concubyn
A twelf month, and excuse hym atte fulle;
And prively a fynch eek koude he pulle.
And if he foond owher a good felawe,
He wolde techen him to have noon awe,
In swich caas, of the erchedekenes curs,
But if a mannes soule were in his purs;
For in his purs he sholde y-punysshed be:
"Purs is the erchedekenes helle," seyde he.
But wel I woot he lyed right in dede.
Of cursyng oghte ech gilty man him drede,
For curs wol slee, right as assoillyng savith;
And also war him of a Significavit.
In daunger hadde he at his owene gise
The yonge girles of the diocise,
And knew hir conseil, and was al hir reed.
A gerland hadde he set upon his heed,
As greet as it were for an ale-stake;
A bokeleer hadde he maad him of a cake.

With hym ther rood a gentil Pardoner
Of Rouncivale, his freend and his compeer,
That streight was comen fro the court of Rome.
Ful loude he soong, "Com hider, love, to me!"
This Somonour bar to hym a stif burdoun;
Was nevere trompe of half so greet a soun.
This Pardoner hadde heer as yelow as wex,
But smothe it heeng as dooth a strike of flex;
By ounces henge his lokkes that he hadde,
And therwith he his shuldres overspradde.
But thynne it lay, by colpons, oon and oon;
But hood, for jolitee, wered he noon,
For it was trussed up in his walét.
Hym thoughte he rood al of the newe jet;
Dischevelee, save his cappe, he rood al bare.
Swiche glarynge eyen hadde he as an hare.
A vernycle hadde he sowed upon his cappe.
His walet lay biforn hym in his lappe,
Bret-ful of pardoun, comen from Rome al hoot.
A voys he hadde as smal as hath a goot.
No berd hadde he, ne nevere sholde have,
As smothe it was as it were late y-shave;
I trowe he were a geldyng or a mare.
But of his craft, fro Berwyk into Ware,
Ne was ther swich another pardoner;
For in his male he hadde a pilwe-beer,
Which that, he seyde, was Oure Lady veyl;
He seyde he hadde a gobet of the seyl
That Seinte Peter hadde, whan that he wente
Upon the see, til Jesu Crist hym hente.
He hadde a croys of latoun, ful of stones,
And in a glas he hadde pigges bones.
But with thise relikes, whan that he fond
A povre person dwellynge upon lond,
Upon a day he gat hym moore moneye
Than that the person gat in monthes tweye;
And thus with feyned flaterye and japes
He made the person and the peple his apes.
But trewely to tellen atte laste,
He was in chirche a noble ecclesiaste;
Wel koude he rede a lessoun or a storie,
But alderbest he song an offertorie;
For wel he wiste, whan that song was songe,
He moste preche, and wel affile his tonge
To wynne silver, as he ful wel koude;
Therefore he song the murierly and loude.

Now have I toold you shortly, in a clause,
Thestaat, tharray, the nombre, and eek the cause
Why that assembled was this compaignye
In Southwerk, at this gentil hostelrye
That highte the Tabard, faste by the Belle.
But now is tyme to yow for to telle
How that we baren us that ilke nyght,
Whan we were in that hostelrie alyght;
And after wol I telle of our viage
And al the remenaunt of oure pilgrimage.

But first, I pray yow, of youre curteisye,
That ye narette it nat my vileynye,
Thogh that I pleynly speke in this mateere,
To telle yow hir wordes and hir cheere,
Ne thogh I speke hir wordes proprely.
For this ye knowen al-so wel as I,
Whoso shal telle a tale after a man,
He moot reherce, as ny as evere he kan,
Everich a word, if it be in his charge,
Al speke he never so rudeliche and large;
Or ellis he moot telle his tale untrewe,
Or feyne thyng, or fynde wordes newe.
He may nat spare, althogh he were his brother;
He moot as wel seye o word as another.
Crist spak hymself ful brode in hooly writ,
And wel ye woot no vileynye is it.
Eek Plato seith, whoso kan hym rede,
"The wordes moote be cosyn to the dede."

Also I prey yow to foryeve it me,
Al have I nat set folk in hir degree
Heere in this tale, as that they sholde stonde;
My wit is short, ye may wel understonde.

Greet chiere made oure Hoost us everichon,
And to the soper sette he us anon,
And served us with vitaille at the beste:
Strong was the wyn and wel to drynke us leste.

A semely man Oure Hooste was with-alle
For to been a marchal in an halle.
A large man he was with eyen stepe,
A fairer burgeys was ther noon in Chepe;
Boold of his speche, and wys, and well y-taught,
And of manhod hym lakkede right naught.
Eek thereto he was right a myrie man,
And after soper pleyen he bigan,
And spak of myrthe amonges othere thynges,
Whan that we hadde maad our rekenynges;
And seyde thus: "Now, lordynges, trewely,
Ye been to me right welcome, hertely;
For by my trouthe, if that I shal nat lye,
I saugh nat this yeer so myrie a compaignye
At ones in this herberwe as is now.
Fayn wolde I doon yow myrthe, wiste I how;
And of a myrthe I am right now bythoght,
To doon yow ese, and it shal coste noght.

"Ye goon to Canterbury—God yow speede,
The blisful martir quite yow youre meede!
And wel I woot, as ye goon by the weye,
Ye shapen yow to talen and to pleye;
For trewely confort ne myrthe is noon
To ride by the weye doumb as a stoon;
And therfore wol I maken yow disport,
As I seyde erst, and doon yow som confort.
And if you liketh alle, by oon assent,
For to stonden at my juggement,
And for to werken as I shal yow seye,
To-morwe, whan ye riden by the weye,
Now, by my fader soule, that is deed,
But ye be myrie, I wol yeve yow myn heed!
Hoold up youre hond, withouten moore speche."

Oure conseil was nat longe for to seche;
Us thoughte it was noght worth to make it wys,
And graunted hym withouten moore avys,
And bad him seye his verdit, as hym leste.

"Lordynges," quod he, "now herkneth for the beste;
But taak it nought, I prey yow, in desdeyn;
This is the poynt, to speken short and pleyn,
That ech of yow, to shorte with oure weye
In this viage, shal telle tales tweye,
To Caunterbury-ward, I mene it so,
And homward he shal tellen othere two,
Of aventúres that whilom han bifalle.
And which of yow that bereth hym beste of alle,
That is to seyn, that telleth in this caas
Tales of best sentence and moost solaas,
Shal have a soper at oure aller cost,
Heere in this place, sittynge by this post,
Whan that we come agayn fro Caunterbury.
And, for to make yow the moore mury,
I wol myselven gladly with yow ryde,
Right at myn owene cost, and be youre gyde;
And whoso wole my juggement withseye
Shal paye al that we spenden by the weye.
And if ye vouche-sauf that it be so,
Tel me anon, withouten wordes mo,
And I wol erly shape me therfore."

This thyng was graunted, and oure othes swore
With ful glad herte, and preyden hym also
That he wolde vouche-sauf for to do so,
And that he wolde been oure governour,
And of our tales juge and réportour,
And sette a soper at a certeyn pris;
And we wol reuled been at his devys
In heigh and lough; and thus, by oon assent,
We been acorded to his juggement.
And therupon the wyn was fet anon;
We dronken, and to reste wente echon,
Withouten any lenger taryynge.

Amorwe, whan that day gan for to sprynge,
Up roos oure Hoost and was oure aller cok,
And gadrede us togidre alle in a flok;
And forth we riden, a litel moore than paas,
Unto the wateryng of Seint Thomas;
And there oure Hoost bigan his hors areste,
And seyde, "Lordynges, herkneth, if yow leste:
Ye woot youre foreward and I it yow recorde.
If even-song and morwe-song accorde,
Lat se now who shal telle the firste tale.
As ever mote I drynke wyn or ale,
Whoso be rebel to my juggement
Shal paye for all that by the wey is spent.
Now draweth cut, er that we ferrer twynne;
He which that hath the shorteste shal bigynne.
Sire Knyght," quod he, "my mayster and my lord
Now draweth cut, for that is myn accord.
Cometh neer," quod he, "my lady Prioresse.
And ye, sire Clerk, lat be your shamefastnesse,
Ne studieth noght. Ley hond to, every man."

Anon to drawen every wight bigan,
And, shortly for to tellen as it was,
Were it by áventúre, or sort, or cas,
The sothe is this, the cut fil to the Knyght,
Of which ful blithe and glad was every wyght;
And telle he moste his tale, as was resoun,
By foreward and by composicioun,
As ye han herd; what nedeth wordes mo?
And whan this goode man saugh that it was so,
As he that wys was and obedient
To kepe his foreward by his free assent,
He seyde, "Syn I shal bigynne the game,
What, welcome be the cut, a Goddes name!
Now lat us ryde, and herkneth what I seye."
And with that word we ryden forth oure weye;
And he bigan with right a myrie cheere
His tale anon, and seyde in this manére.

"""

# Extract final words from the text
final_words = get_final_words(text)

# Check the rhyme type for each couplet (pair of lines)
couplet_rhymes = []
for i in range(0, len(final_words)-1, 2):
    rhyme_type = get_rhyme_type(final_words[i], final_words[i+1])
    couplet_rhymes.append((final_words[i], final_words[i+1], rhyme_type))

# Print the results for each couplet
type_dict = {}
i=1
for word1, word2, rhyme in couplet_rhymes:
    if rhyme == 'F':
        print(f"Words: {word1} and {word2}, {i}")
        print(lines[i-1:i])
    type_dict[i] = rhyme
    i+=2

#print(type_dict)
