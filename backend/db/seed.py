"""
Seed Princeton University tour data.
Called at startup if the cities table is empty.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data definitions
# ---------------------------------------------------------------------------

PRINCETON_DESCRIPTION = (
    "Princeton University, founded in 1746, sits on 600 acres in central New Jersey. "
    "Its compact, walkable campus blends Georgian and Collegiate Gothic architecture "
    "with modern masterpieces. Home to Nobel laureates, US presidents, and some of the "
    "most important research in the world, Princeton consistently ranks among the top "
    "universities globally."
)


@dataclass
class NarrationData:
    depth_tier: str
    script: str
    duration_sec: int


@dataclass
class POIData:
    position: int
    name: str
    tagline: str
    lat: float
    lng: float
    gps_radius_m: int
    walk_note: str | None
    categories: list[str]
    narrations: list[NarrationData] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Nassau Hall
# ---------------------------------------------------------------------------

NASSAU_SNAPSHOT = """Welcome to Nassau Hall — Princeton's oldest building and, for a brief moment, the center of the United States. Built in 1756, this single structure was the entire university. Every lecture, every dorm room, the library, the chapel — all under one roof.

In 1783, the Continental Congress met right here, making Princeton the capital of the new nation. George Washington was formally congratulated here after the British surrender at Yorktown. The bronze tigers flanking the entrance? Princeton students and rival classes have been stealing, painting, and occasionally blowing them up since the 1800s. The tradition continues to this day."""

NASSAU_GUIDE = """Welcome to Nassau Hall — the oldest building at Princeton and one of the most historically significant structures in America. Built in 1756, this was originally the entire university. Every classroom, every dormitory, the library, the chapel — all under one roof. When it was completed, it was the largest building in all of the colonies.

During the Revolutionary War, both British and American forces occupied Nassau Hall. Cannon fire scarred its walls — you can still see where repairs were made in the stonework if you look carefully. In January 1777, General George Washington's forces drove the British out of the building in the pivotal Battle of Princeton. A cannonball reportedly knocked the head off a portrait of King George II hanging inside. Legend says it was replaced with a portrait of Washington himself.

In 1783, the Continental Congress met right here, making Princeton briefly the capital of the new United States. George Washington was formally congratulated here after the British surrender at Yorktown. It's one of those details that gets lost in the sweep of American history — Princeton was, for five months, the seat of the federal government.

The building you see today is largely a reconstruction. A catastrophic fire gutted Nassau Hall in 1802, and another in 1855 left only the exterior walls standing. Each time, it was rebuilt in the same Georgian colonial style — the thick brownstone walls, the symmetrical windows, the central cupola. Robert Smith of Philadelphia designed the original; the restorations maintained his vision.

The bronze tigers flanking the entrance were added in the 1800s, gifts from alumni. Princeton's mascot is the tiger — the origin is somewhat disputed, but the orange and black colors may trace to the House of Nassau, from which Nassau Hall itself takes its name. Since the 1870s, rival classes and competing schools have been stealing, painting, and occasionally blowing up these tigers. Princeton Facilities Management digs them out, re-anchors them, and the cycle begins again. The tradition continues to this day.

Take a moment to walk around to the back of the building. The quiet garden and old cemetery behind Nassau Hall are worth seeing — several early Princeton presidents are buried there, and the pace slows considerably compared to the busy front entrance."""

NASSAU_DEEPDIVE = """Welcome to Nassau Hall — the oldest building at Princeton and one of the most historically significant structures in America.

Built in 1756, Nassau Hall was designed by Robert Smith of Philadelphia and William Shippen of Princeton. At the time of its completion, it was the largest stone building in the colonies — a deliberate statement of ambition by the young College of New Jersey, as Princeton was then known. The structure was named for King William III of the House of Nassau-Orange, who had granted religious tolerance in Britain, a nod to the college's Presbyterian founding principles.

The architectural style is Georgian colonial: thick ashlar brownstone walls quarried locally in New Jersey, symmetrical rows of windows on three stories, a hipped roof, and a central cupola that originally housed the college bell. The proportions are austere, almost severe — nothing like the ornate Gothic buildings that would come later. But that austerity was intentional. This was a building meant to project permanence and gravitas in a colony that was still finding its footing.

The entire College of New Jersey lived and worked inside Nassau Hall for its first decades. The ground floor housed the prayer hall, the library, and the president's quarters. The two upper floors held dormitory rooms — students slept four to a room in conditions we would consider spartan by any modern standard. There was no heating except fireplaces, no plumbing, and the academic day began before dawn. Yet this single building produced graduates who would go on to shape the American republic: James Madison, class of 1771, who became the primary architect of the US Constitution and the fourth President. Aaron Burr Sr., the college's president, and Aaron Burr Jr., who graduated in 1772 and would later kill Alexander Hamilton in a duel. Philip Freneau, the 'Poet of the American Revolution.' William Paterson, who became Governor of New Jersey and an Associate Justice of the Supreme Court.

During the Revolutionary War, Nassau Hall became a military target. Both sides understood its symbolic and strategic value. British forces occupied the building in late 1776, using it as a barracks and stabling horses in the ground floor. In January 1777, George Washington led his forces to Princeton after crossing the Delaware River on Christmas night. The Battle of Princeton, fought on January 3, 1777, was a turning point in the war — one of Washington's most daring tactical maneuvers. British troops retreated into Nassau Hall, barricading the doors. American forces brought up a cannon — commanded, some accounts say, by the young Alexander Hamilton — and fired into the building. One cannonball reportedly passed through a window and decapitated a portrait of King George II hanging in the prayer hall. The British surrendered. That portrait was later replaced with the earliest known portrait of George Washington as president, painted by Charles Willson Peale, which still hangs in the Faculty Room today.

The Continental Congress met in Nassau Hall from June to November 1783, making Princeton the de facto capital of the United States for five months. Congress fled Philadelphia after mutinous Pennsylvania troops surrounded the State House demanding back pay — Princeton offered a safer location. It was here that Congress received news of the final peace treaty with Britain, and here that Washington was formally thanked by the young nation for his service. He reportedly gave a brief, gracious reply and nothing more. The building where this happened looks nearly the same today as it did then.

Two fires tested Nassau Hall's resilience. The first, in 1802, gutted much of the interior. The second, in 1855, was more severe — only the exterior walls survived. Each time, Benjamin Henry Latrobe (after the first fire) and John Notman (after the second) rebuilt the interior while maintaining the original Georgian exterior. The brownstone walls you see today are largely original 18th-century construction. The cupola was rebuilt and the bell rehung, though the original bell — which had been captured by British forces during the occupation — was never recovered.

Walk around to the rear of Nassau Hall. Behind the building lies a quiet garden and a small cemetery where several early Princeton presidents are buried, including Jonathan Dickinson, the college's first president, and Aaron Burr Sr. The cemetery is one of the oldest in New Jersey and a striking contrast to the busy main entrance. The rear lawn was the site of informal student life for two centuries — a tradition of gathering, debating, and the occasional spontaneous bonfires that university administrators regarded with mixed feelings.

The bronze tigers at the front entrance were gifts from alumni, added in different decades as the tiger became Princeton's unofficial mascot. The orange and black colors most likely derive from the House of Nassau — William of Orange's heraldic colors — though the connection was retroactively formalized in the late 19th century. Since the 1870s, the tiger statues have been the object of elaborate pranks: painted by rivals, stolen, replaced with replicas, and, in at least one documented incident in the early 20th century, damaged by a small explosive device. Princeton Facilities Management treats this as an ongoing operational reality. The tigers are periodically re-anchored in concrete, and the cycle continues. It is, in its way, one of the oldest living traditions on campus."""

# ---------------------------------------------------------------------------
# Maclean House
# ---------------------------------------------------------------------------

MACLEAN_SNAPSHOT = """This modest Georgian house is the oldest surviving building on campus — and it has housed every Princeton president for 270 years. Woodrow Wilson lived here from 1902 to 1910, governing Princeton before going on to govern New Jersey, then the United States. By Ivy League standards, it's refreshingly unpretentious. Very Princeton."""

MACLEAN_GUIDE = """Welcome to Maclean House — the oldest surviving building on Princeton's campus, and the official residence of Princeton's president since 1756. While Nassau Hall across the path gets most of the historical attention, this quiet Georgian house has been continuously occupied for nearly 270 years.

Built at the same time as Nassau Hall, Maclean House was originally the home of the college president. Jonathan Dickinson, Princeton's founding president, and Aaron Burr Sr., his immediate successor, both lived here. The house takes its current name from John Maclean Jr., Princeton's 11th president, who served from 1854 to 1868 and presided over the college during the Civil War years.

The most famous occupant, by historical weight, is Woodrow Wilson. Wilson lived in Maclean House from 1902 to 1910, during his tenure as Princeton's 13th president. His eight years here were transformative for the university. He introduced the preceptorial system — small-group tutorials modeled on Oxford — which fundamentally changed how Princeton taught its students. He reorganized the academic departments, created the modern residential college concept, and elevated Princeton's academic reputation dramatically.

Wilson left Maclean House in 1910 to run for Governor of New Jersey, won, then ran for President of the United States in 1912, and won that too. He was the only US president to hold a PhD, and Princeton is where he did much of his intellectual formation. The parallels between his administrative style at Princeton — idealistic, occasionally inflexible, brilliant — and his presidency of the United States are striking and well-documented by historians.

The architecture of Maclean House is Georgian vernacular: simpler and more domestic than the formal Georgian of Nassau Hall. The proportions are human-scaled, the details restrained. It is a house, not a monument — which is precisely what makes it interesting. It has survived two centuries of campus expansion, new construction on all sides, and the constant churn of university life without being dramatically altered.

Today Maclean House serves as the official residence and meeting space for Princeton's president, and is not generally open to the public. But the exterior, the surrounding garden, and its position at the heart of the historic campus repay a few minutes of quiet observation."""

MACLEAN_DEEPDIVE = """Maclean House stands as the oldest continuously occupied building on Princeton's campus — a distinction that is easy to overlook given the grander presence of Nassau Hall just steps away.

The house was built in 1756, the same year as Nassau Hall, and designed in the Georgian vernacular style — domestic rather than monumental, with symmetrical windows, a central doorway, and proportions that suggest a prosperous colonial household rather than an institutional building. The original construction used local Jersey brownstone, the same material as Nassau Hall, giving the two buildings a visual kinship that anchors the historic core of the campus.

Jonathan Dickinson, Princeton's first president, was supposed to have lived here, but he died in 1747 — nine years before the building was completed, and before the College of New Jersey had even moved from Newark to Princeton. Aaron Burr Sr., the second president and father of the famous duelist, was effectively the first occupant. He died in 1757, a year after the building was completed, having exhausted himself establishing the college in its new home. Samuel Davies, the fourth president, called the house 'the most agreeable habitation I have seen in America,' which says something either about the house or about the state of colonial American domestic architecture.

The building takes its name from John Maclean Jr., Princeton's 11th president (1854–1868). Maclean was a Princeton lifer — born in Princeton, educated at Princeton, and served the university in various capacities for decades before becoming president. His tenure spanned the Civil War, a period of enormous stress for American institutions. Princeton had strong ties to the South — a significant fraction of its students before the war were from Southern families — and Maclean navigated the political tensions with considerable difficulty. The university remained open throughout the war, though enrollment dropped sharply.

Woodrow Wilson's occupancy from 1902 to 1910 is the chapter that most shapes how historians remember the house. Wilson came to Princeton as its 13th president after a distinguished career as a political scientist and author. His first years were a burst of institutional creativity. The preceptorial system he introduced in 1905 — bringing 50 new faculty preceptors to teach in small groups of two or three students — was modeled explicitly on Oxford's tutorial system and was genuinely revolutionary for American higher education at the time. Wilson believed that Princeton's undergraduates were being processed rather than educated, and he set out to change that.

His proposed 'Quad Plan' — to reorganize student housing into residential quadrangles and abolish the eating clubs that dominated undergraduate social life — was more controversial. The eating clubs along Prospect Avenue (you'll see them later on the tour) were deeply embedded in Princeton's social fabric, and many alumni and trustees opposed the plan fiercely. Wilson's inflexibility on the issue, combined with a separate conflict with Dean Andrew West over the location of the Graduate College, ultimately led to his break with Princeton. He resigned in 1910 to run for Governor of New Jersey — a race he won — and two years later won the presidency of the United States.

The intellectual and psychological parallels between Wilson's Princeton presidency and his US presidency have fascinated biographers. The same visionary ambition, the same rhetorical brilliance, the same unwillingness to compromise that ultimately doomed the League of Nations — all were visible in miniature during his years at Maclean House. John Milton Cooper Jr.'s biography 'Woodrow Wilson' treats Princeton as the laboratory in which Wilson's political personality was fully formed.

Architecturally, Maclean House has been modified carefully over the centuries but retains its essential 18th-century character. The interior — not accessible to the public — includes a formal reception room used for presidential meetings and events, a dining room that has hosted heads of state and Nobel laureates, and private quarters that remain essentially domestic in scale. The garden surrounding the house has been replanted multiple times but maintains an informal, residential character that contrasts with the more formal landscaping elsewhere on the historic campus.

Compared to other Ivy League presidential residences — Harvard's Elmwood, Yale's Woodbridge Hall — Maclean House is notably modest. It was not designed to impress; it was designed to house a working academic administrator. That modesty is, paradoxically, what makes it impressive today. It has been home to some of the most consequential figures in American intellectual and political life, and it looks like a house."""

# ---------------------------------------------------------------------------
# Princeton University Art Museum
# ---------------------------------------------------------------------------

ART_MUSEUM_SNAPSHOT = """One of the finest university art museums in the world — and admission is free. The collection spans 115,000 works across 5,000 years of human civilization. The building itself is brand new: dramatically renovated and reopened in 2023 with a stunning light-filled atrium that transformed what was once a cramped Victorian structure into one of the great museum spaces on the East Coast."""

ART_MUSEUM_GUIDE = """Welcome to the Princeton University Art Museum — consistently ranked among the finest university art museums in the world, and free to the public every day it's open.

The collection is extraordinary in its scope: over 115,000 objects spanning 5,000 years, from ancient Egyptian artifacts to contemporary works acquired last year. For a collection that started with a handful of plaster casts in the 1880s, its current depth and quality reflects more than a century of strategic acquisitions, remarkable donations, and serious scholarship.

The highlights span every department. The Asian art collection is among the strongest at any university, particularly the Chinese bronzes and ceramics. The collection of Greek and Roman antiquities includes pieces that would anchor a standalone antiquities museum. There are medieval European works, old masters, and a particularly strong holding of 19th and 20th century American and European paintings. The photography collection, established early and built deliberately, is world-class.

The building you're looking at is the result of a dramatic renovation completed in 2023. The original structure dated from 1966, with earlier portions even older, and had been through a series of additions that left the museum somewhat cramped and awkward. The 2023 project — designed by David Adjaye of Adjaye Associates — gutted and reconceived the interior around a soaring central atrium flooded with natural light. The renovation won immediate architectural praise and transformed the museum's relationship to the campus and to visitors.

The museum is open Tuesday through Sunday, closed Mondays. Admission is always free — no timed tickets, no reservations required for general admission. If you have time to go inside, do."""

ART_MUSEUM_DEEPDIVE = """The Princeton University Art Museum holds one of the most significant art collections in the United States — a status that is not always fully appreciated outside the art world, where the museum operates somewhat in the shadow of its metropolitan counterparts.

The collection's origins are modest. In 1882, Princeton received a gift of plaster casts of ancient sculpture — the standard 19th-century educational tool for teaching classical art history without actual classical art. The cast collection grew, and with it grew the ambition for something more. By the early 20th century, Princeton alumni and faculty had begun giving and acquiring original works, and the museum's scope began expanding in earnest.

Today the collection numbers more than 115,000 objects spanning five millennia and six continents. The range is genuinely encyclopedic: ancient Near Eastern cylinder seals, Egyptian funerary objects, Greek red-figure pottery, Roman portrait busts, Byzantine icons, medieval European ivories, Renaissance paintings, old master drawings, Asian ceramics and bronzes, African sculpture, pre-Columbian goldwork, European paintings from the 15th through 20th centuries, American paintings from the colonial period to the present, modern and contemporary art, photography, and prints and drawings.

Several departments stand out as exceptional even by major museum standards. The Chinese bronze collection is among the finest outside Asia, representing ritual vessels from the Shang and Zhou dynasties (roughly 1600–256 BCE) that were acquired when such pieces were more available on the market. The Greek and Roman collection includes not just decorative arts but significant sculptural works, including pieces that scholars use as reference points for understanding ancient artistic production. The photography collection, built systematically from the medium's earliest years, holds works by every major figure in the medium's history.

In terms of individual works, the museum holds paintings by Monet, Cézanne, Picasso, Warhol, and Ellsworth Kelly, among hundreds of others. The old master drawings collection includes sheets by Raphael, Michelangelo, and Rembrandt. The Guatemalan colonial collection — rarely exhibited at other institutions — is one of the deepest in North America.

The 2023 renovation, designed by David Adjaye of Adjaye Associates, is the museum's most significant transformation since its founding. The original 1966 building by Steinmann, Cain & White had been expanded with awkward additions in 1989 and 2007, leaving the museum with poor circulation, inadequate natural light, and a spatial logic that confused visitors. Adjaye's solution was radical: he gutted the interior and replaced it with a new structure organized around a 70-foot-tall central atrium covered by a faceted skylight that floods the galleries with natural light. The atrium functions as both circulation spine and gathering space, creating a social center for the museum that the old building entirely lacked.

The renovation also expanded the museum's total square footage by roughly 40 percent, nearly doubled gallery space, and added a new education wing, conservation facilities, and storage. The exterior retained and restored the original 1966 facade on the Nassau Street side while adding a new glass-and-stone entrance pavilion. The result has been widely praised: the New York Times called it 'a transformation,' and the renovation won the 2024 AIA Institute Honor Award for Architecture.

The museum is free to the public every day it is open (Tuesday through Sunday, closed Monday). This is not a token gesture — there are no 'suggested donations' for general admission, no timed-entry tickets for the permanent collection, no premium access tiers. It is simply free. For a collection of this quality, in a building of this quality, it is one of the great bargains in American cultural life.

If you visit, recommended must-see works depend on your interests: for ancient art, the Chinese bronzes in Gallery 15 and the Greek vases in Gallery 5; for paintings, the Impressionist works on the second floor and the American paintings from the Federal period; for photography, the rotating exhibitions in the dedicated photography galleries are almost always exceptional."""

# ---------------------------------------------------------------------------
# University Chapel
# ---------------------------------------------------------------------------

CHAPEL_SNAPSHOT = """The third largest university chapel in the world. Completed in 1928. Seats 2,000 worshippers. The Gothic architecture was modeled explicitly on the great English cathedrals, and the attention to craft — carved stonework, stained glass, hand-carved choir stalls — is extraordinary. Albert Einstein, who spent his later career at the nearby Institute for Advanced Study, occasionally attended lectures and concerts here."""

CHAPEL_GUIDE = """Welcome to Princeton University Chapel — the third largest university chapel in the world, behind only those at Valparaiso University and Washington National Cathedral.

Completed in 1928 after four years of construction, the chapel seats 2,000 and dominates the western edge of the historic core of campus. It is, by any measure, an extraordinary building. The Gothic architecture was designed by Ralph Adams Cram, the most influential ecclesiastical architect of the early 20th century, and it draws explicitly on the great medieval English cathedrals — particularly the English Perpendicular Gothic of Winchester and York.

The scale is immediate and overwhelming when you enter. The nave stretches 250 feet from entrance to chancel. The ceiling vaults rise 76 feet. Every surface rewards close attention: carved stone figures in the nave arcades, hand-carved wooden choir stalls with misericords depicting figures from Princeton's history, and stained glass windows that rank among the finest examples of the craft made in the 20th century.

Princeton was founded as a Presbyterian institution, and the chapel reflects that heritage — though the university has been officially non-sectarian since 1868, and today welcomes students of all faiths and none. Services, concerts, lectures, and memorial events are held here throughout the academic year. The acoustic quality is remarkable — the building was designed with performance in mind, and some of the finest musicians in the world have performed here.

Albert Einstein, who spent his later career at the nearby Institute for Advanced Study just off campus, occasionally came to Nassau Hall for lectures. By some accounts he attended a concert or two at the chapel, though he was not religious. His presence at Princeton from 1933 until his death in 1955 is one of those biographical details that makes the campus feel haunted by history."""

CHAPEL_DEEPDIVE = """Princeton University Chapel is one of the finest Gothic Revival buildings in the United States — a statement that would have pleased its architect enormously and that remains essentially unchallenged a century after its construction.

Ralph Adams Cram designed the chapel beginning in 1924, and it was completed and dedicated in 1928. Cram was the dominant figure in American ecclesiastical architecture for four decades, responsible for the continued construction of the Cathedral of St. John the Divine in New York and dozens of other significant Gothic Revival buildings. He believed passionately that Gothic was not merely a historical style but the highest achievement of Western architecture — structurally logical, spiritually elevating, and capable of accommodating the full range of human artistic craft.

At Princeton, Cram was given the latitude to execute his vision at full scale. The chapel is 253 feet long, 76 feet tall in the nave, and 2,000 seats wide at full capacity. The plan is a traditional Latin cross: nave, transept, chancel, and apse. The exterior is Millstone Valley granite, cut and laid in courses that vary slightly in color and texture — deliberately, to avoid the mechanical uniformity of precisely matched stone. The effect in afternoon light is extraordinary: the walls seem almost to breathe.

The model was explicitly English Perpendicular Gothic — the style of Winchester Cathedral, of King's College Chapel at Cambridge, of the Henry VII chapel at Westminster Abbey. Cram studied these buildings firsthand and incorporated specific details: the large clerestory windows flooding the nave with light, the fan-like tracery of the window heads, the shallow pitched rooflines over the aisles. But he adapted rather than copied. The building is American in its materials, its scale, and its deliberate synthesis of multiple Gothic traditions rather than strict adherence to one period.

The stained glass windows are among the greatest achievements of the building. The nave windows were designed by various studios over several decades — the Willet Studios of Philadelphia made the largest and most significant of them, including the great west window and the rose window over the entrance. The colors were carefully chosen to create a specific quality of light at different times of day: cool and blue in the morning hours, warming to gold and amber in the afternoon. Each window depicts narrative scenes from scripture and from Christian history, with additional panels honoring Princeton alumni who died in the World Wars.

The carved wooden choir stalls deserve extended attention. Made of hand-carved oak by master craftsmen, the stalls include misericords — the small wooden ledges on the underside of the hinged seats that allowed medieval choristers to 'half-sit' during long services. Princeton's misericords depict not biblical scenes but figures from the university's own history: presidents, alumni, scenes of campus life. It is a quietly democratic touch in an otherwise solemn building.

Albert Einstein's connection to Princeton is one of the most celebrated in the university's history, though it is technically an Institute for Advanced Study connection rather than a university one. The Institute, founded in 1930, is a separate organization located on its own campus a short walk from the university, and Einstein joined it in 1933 when he fled Germany after the Nazi rise to power. He lived in Princeton until his death in 1955. During those 22 years, he became part of the fabric of the town — riding his bicycle through campus, attending lectures at Fine Hall, occasionally appearing at public events. He was not a religious man (his 'cosmic religion' was pantheistic rather than theistic), but he is documented to have attended at least one memorial service in the chapel and several concerts. The building's scale and craft seem precisely the kind of thing that would have interested him: large problems solved with elegant structural logic.

Princeton's relationship with religion is long and complicated. The college was founded in 1746 by New Side Presbyterians as a training ground for clergy — though from the beginning it also educated men who had no intention of becoming ministers. The shift to official non-sectarianism came in 1868, under the presidency of James McCosh. By the time the chapel was built in the 1920s, Princeton's religious identity was already ecumenical in practice if not always in self-description. Today the chapel holds services across multiple Christian denominations, as well as Jewish High Holiday services, Muslim Friday prayers, and interfaith memorial events. The building's Gothic grandeur, designed for a specific theological tradition, has proved adaptable to this broader purpose — which Cram, who was a committed Anglo-Catholic, might have found ironic.

The chapel's acoustic properties are exceptional and were carefully engineered. The reverberation time — the duration of sound decay in the space — is approximately 4.5 seconds in an empty chapel and roughly 2.5 seconds when filled with people. This is ideal for choral and organ music, slightly challenging for speech without amplification. The Mander organ, installed in 2000 and replacing an earlier instrument, is considered one of the finest in the United States: 9,000 pipes, four manuals, and a tonal design that suits both liturgical and concert use. The chapel has hosted performances by the Tallis Scholars, the King's Singers, the Vienna Philharmonic Chorus, and soloists of the highest caliber."""

# ---------------------------------------------------------------------------
# Blair Arch
# ---------------------------------------------------------------------------

BLAIR_SNAPSHOT = """The most photogenic spot on campus, and possibly the most acoustic. Completed in 1897, Blair Arch connects Blair Hall's two Gothic wings with a massive carved stone archway. Princeton's a cappella groups perform here — the stone walls create a natural reverb chamber that has to be heard to be believed. Walk through slowly."""

BLAIR_GUIDE = """Welcome to Blair Arch — the most photographed spot on Princeton's campus, and for good reason. The massive Gothic stonework, the careful proportions, the way it frames Nassau Hall in the distance — it's a composition that looks designed for photography, even though it was built decades before photography was common.

Blair Arch was completed in 1897, designed by architect William Potter. It connects the two wings of Blair Hall — one of Princeton's first residential dormitories and part of the campus's transition toward the residential college model. The arch itself is a tour de force of Collegiate Gothic stonework: limestone carved with elaborate tracery, heraldic shields, and figures that reward close inspection. The vault springs from corbels carved with faces — some serene, some grimacing, some apparently laughing. Medieval cathedral builders put their best stone carvers on the high work where few would see it clearly; Princeton's craftsmen lavished the same care on details at eye level.

The residential college system the arch represents was Princeton's deliberate adoption of the Oxford and Cambridge model — breaking the large university into smaller social units where students live, eat, and engage with faculty in more intimate settings. Blair was one of the first buildings constructed for this purpose, and the arch was designed to serve as a ceremonial gateway between the older academic core and the new residential buildings.

The acoustic properties of the arch are remarkable and are the reason Princeton's a cappella groups perform here. The stone walls, the curved vault, and the specific geometry of the space create a reverb chamber that enhances voices without overwhelming them. Groups have been singing here since the arch was built. Walk through slowly and you'll hear the space change as you move — drier at the edges, richer at the center.

Turn around when you're on the far side: the view back through the arch toward Nassau Hall, framed by Blair's towers, is precisely the view that photographers seek and that appears in every Princeton brochure. The campus's architectural coherence — a relatively rare achievement in American universities, where building campaigns happen across different eras and aesthetic fashions — is nowhere more visible than from this vantage point."""

BLAIR_DEEPDIVE = """Blair Arch stands at the intersection of two defining narratives in Princeton's architectural history: the adoption of Collegiate Gothic as the campus's dominant style, and the development of the residential college system that fundamentally shaped undergraduate life.

The arch was designed by William A. Potter and completed in 1897. Potter had been a significant figure in American Gothic Revival architecture since the 1870s, designing churches, civic buildings, and early collegiate structures. His work at Princeton was part of a broader effort to give the campus a coherent architectural identity — an effort that would culminate in the master plan adopted under Woodrow Wilson's presidency.

The Collegiate Gothic style Potter employed at Blair was a deliberate synthesis: English Perpendicular Gothic in its structural logic and decorative vocabulary, but adapted to the materials and building technologies of late 19th-century America. The limestone used at Blair is lighter in color than the brownstone of Nassau Hall, giving the newer buildings a different visual temperature — cooler, more silvery — that still harmonizes with the older structures. The Gothic details — pointed arches, carved tracery, crenellated parapets, corner turrets — are executed with considerable craftsmanship. Some of the carved figures in the spandrels and corbels repay close inspection: medieval craftsmen's tradition of humor and self-reference appears here, with faces that range from idealized to comic.

The arch itself is a tunnel vault rather than a pointed arch in the structural sense — the vault springs from corbels on each side and meets at the crown with carved keystone figures. The geometry was not accidental: it creates the acoustic chamber that makes the space remarkable for music. The reverberation in the arch is roughly 1.5 to 2 seconds — shorter than the chapel's cathedral-scale reverb, but longer than an open courtyard. For unaccompanied voices, this length is nearly ideal: long enough to blend harmonics, short enough to preserve clarity.

Princeton's a cappella tradition is among the oldest and most active in American collegiate music. The oldest group, the Nassoons, was founded in 1941. Since then, more than a dozen groups have formed across musical styles — classical, barbershop, contemporary pop, gospel. Blair Arch has been their primary performance venue not merely by convention but because the acoustics are genuinely better here than anywhere else on campus. Groups hold casual performances called 'audits' at the arch throughout the academic year; the formal season runs from September through April. Hearing a group here on a clear autumn evening, with the Gothic stonework lit and the campus quiet, is one of those Princeton experiences that undergraduates remember for decades.

The view from the far side of the arch — looking back through the opening toward Nassau Hall — is one of the defining images of the campus and of American collegiate architecture more broadly. It appears on admissions materials, alumni publications, and in countless photographs. What makes it work architecturally is the layering: the arch frames Blair Hall's towers, which frame the sky, and through the archway Nassau Hall appears in the middle distance, its Georgian proportions contrasting with the Gothic surround. The depth of field, the play of stone colors, the way the scene changes with the light — morning is cool and sharp, afternoon is warm and almost cinematic — is the result of a campus planned with unusual coherence.

Princeton's campus is frequently cited as one of the most architecturally unified in America, and the reasons are worth understanding. In 1906, under Woodrow Wilson, the university commissioned a master plan that designated Collegiate Gothic as the required style for all new construction. This was an extraordinary act of institutional discipline: it meant that every building added to the historic core for the next several decades had to conform to a set of stylistic principles, regardless of function, scale, or the architectural fashions of the moment. The plan was not perfectly followed — some buildings from the 1950s and 60s are aggressively modernist — but the Gothic core has remained remarkably coherent. Blair Arch, built nine years before the formal master plan, was the precedent that the plan formalized.

The residential college system Blair Hall represents was modeled explicitly on Oxford and Cambridge — a fact Wilson stated openly and frequently. The goal was to counteract what Wilson saw as the fragmentation of university life: students eating in eating clubs organized by social class, forming friendships primarily within narrow social networks, and failing to engage seriously with academic life outside the classroom. The residential college would provide the alternative social structure. Each college would house students from all four years, provide dining and social space, and appoint faculty fellows who would live and work among the students. The eating clubs on Prospect Avenue survive and remain influential, but the residential college system Wilson imagined was eventually implemented and is now central to Princeton's undergraduate experience."""

# ---------------------------------------------------------------------------
# Prospect House & Gardens
# ---------------------------------------------------------------------------

PROSPECT_SNAPSHOT = """This Italianate villa, built in 1849, was Woodrow Wilson's home when he served as Princeton's president from 1902 to 1910. He left here to become Governor of New Jersey, then President of the United States. The formal English gardens behind the house are free and open to the public year-round — one of the best-kept secrets on campus."""

PROSPECT_GUIDE = """Welcome to Prospect House — an Italianate villa built in 1849 and one of the few genuinely grand private residences that became part of the Princeton campus.

The house was built for John Potter Stockton, a member of one of New Jersey's most prominent families, and acquired by the university in 1878. It has served as the official president's residence since then — though Maclean House, which you saw earlier, was also used by some presidents. The distinction: Prospect House is grander, more formal, used for receptions and official entertainment, while Maclean House was more domestic.

The most famous occupant is again Woodrow Wilson, who lived here from 1902 to 1910. During those eight years he transformed Princeton's academic structure and fought the famous battles over the Quad Plan and the Graduate College location that ultimately led to his departure. The house's formal dining room was the setting for many of the faculty dinners and trustee meetings where these battles played out.

Wilson left Prospect House in 1910 to campaign for Governor of New Jersey — a race he won with a remarkable margin. Two years later he won the presidency of the United States. He is the only sitting university president to have made the leap directly to a state governorship and then the White House.

The Prospect Garden behind the house is what most visitors come for today. Designed in the English formal garden tradition, it's organized around a central path flanked by seasonal plantings — roses in summer, chrysanthemums in fall, tulips in spring. The garden is free, always open, and consistently lovely. It's one of the places on campus where the pace of academic life slows to something more contemplative.

The Italianate architecture of the house itself — the wide overhanging eaves, the low-pitched roof, the bracketed cornice, the tall narrow windows — was fashionable in the 1840s and reflects the influence of Andrew Jackson Downing, the landscape designer who popularized the style for American country houses."""

PROSPECT_DEEPDIVE = """Prospect House occupies a singular position in Princeton's physical and institutional history: it is the grandest private house ever incorporated into the campus, and it has been at the center of some of the university's most consequential decisions.

The house was built in 1849 for John Potter Stockton, whose family had been among the most prominent in New Jersey since the colonial era. Richard Stockton, John's grandfather, had signed the Declaration of Independence. The family's connection to Princeton was deep — multiple Stocktons had attended the college, and the family seat, Morven (now a New Jersey state historic site), stood nearby. Prospect was built as a country villa, and the Italianate style Stockton chose reflected the influence of Andrew Jackson Downing, whose pattern books had made the style fashionable for prosperous American families seeking houses that combined picturesque informality with domestic comfort.

The Italianate details are visible throughout the exterior: wide overhanging eaves supported by decorative brackets, low-pitched roofs, tall narrow windows with elaborately molded hoods, a square cupola that originally provided views across the campus and surrounding countryside. The massing is asymmetrical — towers of different heights, wings extending in different directions — in deliberate contrast to the formal symmetry of Georgian buildings like Nassau Hall. The effect was meant to suggest a natural relationship between house and landscape, a building that had grown organically rather than been imposed.

The university acquired Prospect in 1878, three years after the Stockton estate sold it. The purchase was motivated partly by the university's need for a more impressive presidential residence — Maclean House had served for 120 years but was modest by the standards of what peer institutions were providing their presidents — and partly by the desirability of the land, which gave the university control over the south end of the campus and the approach from Nassau Street.

The house served as the primary presidential residence from 1878 onward, with the president's family occupying the private rooms and the formal spaces used for official entertainment. The dining room — a high-ceilinged room on the south side of the house — was the setting for faculty dinners, trustee meetings, and the informal conversations that shaped university policy. It was here, over many dinners between 1902 and 1910, that Woodrow Wilson built the alliances and encountered the opposition that defined his Princeton presidency.

Wilson's tenure at Prospect is worth examining in detail. He arrived in 1902 with a mandate for academic reform and extraordinary personal ambition. His first major initiative, the preceptorial system of 1905, was a success — 50 new faculty were hired, teaching methods were transformed, and Princeton's academic reputation rose sharply. His second initiative, the Quad Plan of 1907, was a failure that nonetheless revealed something important about the university's power structure. Wilson proposed abolishing the eating clubs on Prospect Avenue and replacing them with Oxford-style residential quadrangles where students from all social backgrounds would mix. The eating clubs had been the center of Princeton's social life since the 1870s, and many alumni had deep loyalties to them. The trustees ultimately rejected the plan, and Wilson's relationship with the board began its deterioration.

The third conflict — over the location and governance of the Graduate College — was the decisive one. Wilson wanted the graduate students integrated into the undergraduate campus; Dean Andrew West wanted a separate, autonomous graduate community at the edge of campus. West won, thanks largely to a $10 million gift from a donor who specified West's preferred location. Wilson resigned in 1910.

He ran for Governor of New Jersey and won with 54 percent of the vote, a remarkable margin for a man who had never held elected office. Two years later, the Democrats nominated him for president. He won the three-way race against William Howard Taft and Theodore Roosevelt with 41.8 percent of the popular vote and 435 electoral votes. He served two terms, overseeing entry into World War I and attempting, with famous failure, to bring the United States into the League of Nations.

The Prospect Garden behind the house was redesigned multiple times after the university acquired the property. The current garden reflects a redesign from the early 20th century, organized in the English formal tradition: a central axis with cross paths dividing the space into quadrants, each planted with seasonal flowers chosen for successive bloom times. The garden is maintained by the university's grounds department and is one of the most carefully tended spaces on campus. The rose garden, at its peak in late June, is exceptional. The garden is free and open to the public year-round, without admission or reservation.

Today Prospect House serves as the faculty club — a function it has held since 1954, when the president moved permanently to Lowrie House on Library Place. Faculty members eat lunch here on weekdays, and the formal rooms are used for departmental events, alumni gatherings, and receptions. The transition from presidential residence to faculty club is, in retrospect, very Princeton: the grandest house on campus became a place where the professors eat lunch."""

# ---------------------------------------------------------------------------
# Cannon Green
# ---------------------------------------------------------------------------

CANNON_SNAPSHOT = """A Revolutionary War cannon, captured in the Battle of Princeton in January 1777, now buried here with only its muzzle visible. Students have been trying to bury it completely or paint it since the 1870s. Princeton maintenance digs it back out and repaints it. This has been happening continuously for 150 years. It shows no sign of stopping."""

CANNON_GUIDE = """Welcome to Cannon Green — and to one of the more peculiar ongoing situations in American academic life.

The cannon buried in the center of this green was captured during the Battle of Princeton on January 3, 1777 — one of George Washington's most tactically brilliant victories in the Revolutionary War. After the battle, the cannon remained on campus as a trophy. In 1840, students buried it in this spot, leaving only the muzzle showing. The rationale is lost to history; it simply seemed like the thing to do.

Since the 1870s, Princeton's ongoing class rivalries have centered on the cannon. Sophomores try to paint it their class color; freshmen try to bury it completely (which is very difficult, since it's anchored in concrete). Rival institutions — particularly Rutgers, Princeton's oldest rival — have attempted to steal it multiple times. There have been painted cannonballs, decoy cannons, concrete poured over the muzzle, and at least one occasion where someone welded a lid over the opening. Princeton Facilities Management excavates, repaints the black paint, re-anchors as needed, and the cycle resumes.

The green itself — the lawn surrounded by Gothic residential buildings on three sides — is one of the social hearts of campus. This is where students throw frisbees and study outdoors in good weather, where Reunions events spill out from the buildings, and where Class Day is celebrated each May. The Gothic buildings that surround it were built between the 1890s and 1910s, and the enclosure they create gives the green an almost cloister-like quality.

From here, you've completed Princeton's historic core. Nassau Hall is visible to the north — you've come full circle. If you have additional time, Firestone Library, just east of here, holds one of the great research collections in the world and is worth a look inside. The entrance hall alone, with its murals, is worth a few minutes."""

CANNON_DEEPDIVE = """The cannon buried in the center of Cannon Green connects Princeton's present to one of the most consequential days of the American Revolution — and then, through an unbroken chain of tradition and stubbornness, to every Princeton class since 1840.

The Battle of Princeton was fought on January 3, 1777, eight days after Washington's famous crossing of the Delaware on Christmas night. Washington had surprised and defeated the Hessian garrison at Trenton on December 26, then maneuvered brilliantly to outflank the main British force under Cornwallis. Rather than retreating across the Delaware again, he marched his army north overnight along a back road, bypassing the British lines, and struck the British garrison at Princeton from the south.

The battle lasted roughly 45 minutes. The British forces, caught off-guard, fought back hard — the initial American advance under General Mercer was repulsed and Mercer was mortally wounded. Washington personally led a counterattack, riding to within 30 yards of the British line and rallying his troops while musket fire cracked around him. The British broke, and the remnants fled north toward New Brunswick. American forces captured the Nassau Hall stronghold, securing the town. Several British cannon were taken as trophies.

One of those cannon eventually made its way to this spot. It remained above ground on the campus for several decades, used occasionally as a prop in student celebrations and as the object of periodic informal competition. In 1840, for reasons that are not fully documented in the historical record — the best available evidence suggests it began as a sophomore class prank that simply stuck — students buried the cannon with its muzzle pointing upward, leaving roughly six inches of metal visible above the surface.

The tradition of rivalry around the cannon became formalized in the 1870s as Princeton developed its class system and its culture of inter-class competition. Sophomores, by longstanding custom, were responsible for 'maintaining' the cannon — which in practice meant painting it black and defending it from freshmen, who were supposed to try to bury it completely. The rationale was never entirely serious; the point was the tradition itself, the annual re-enactment of a competition whose origins were already obscure.

The cannon has been the object of some genuinely elaborate operations. Rutgers University, Princeton's oldest rival (the schools played the first intercollegiate football game in 1869), mounted several retrieval attempts in the late 19th and early 20th centuries. The most determined of these, around 1875, involved a team of Rutgers students arriving at night with digging equipment; they were discovered and chased off before reaching the cannon. Princeton subsequently anchored the cannon in concrete. Subsequent attempts have involved painted cannonballs placed nearby (as decoys or replacements), concrete poured into the muzzle, and in one case — exact date disputed — a metal lid welded over the opening.

Princeton Facilities Management addresses these interventions matter-of-factly. The cannon is excavated as needed, the paint stripped and re-applied (gloss black is the standard), and any structural damage to the surrounding green repaired. Staff members who have worked in the department for decades report that cannon maintenance is simply an accepted part of the annual cycle, like repainting the Pyne-Mathey courtyard before Reunions.

The surrounding green — enclosed by Pyne Hall (1922), Henry Hall (1907), and other Gothic residential buildings — provides context for the cannon's peculiar prominence. The buildings were constructed as part of the residential college expansion under Woodrow Wilson's master plan, using the same limestone and Gothic vocabulary as Blair Arch and the Chapel. The enclosure they create is genuinely cloister-like: the noise of Nassau Street and the surrounding campus falls away inside the green, and the sense of being in a self-contained precinct is pronounced.

Cannon Green serves as one of the primary outdoor social spaces of the campus. In good weather, it is used for frisbee, outdoor study, informal music, and spontaneous gatherings. During Reunions — Princeton's reunion weekend in late May, famously one of the largest and most festive in American higher education — the green is the site of outdoor events, bands, and the procession of returning alumni in orange-and-black costumes. Class Day, the undergraduate celebration on the eve of Commencement, centers on the green: the class president speaks from steps near the cannon, and the assembled seniors hear final remarks before going their separate ways.

The view north from Cannon Green, back toward Nassau Hall, closes the loop of the historic campus tour. You can trace the buildings you've visited from here: Nassau Hall and Maclean House to the north, the Art Museum towers to the east, the Chapel spire to the west, Blair Arch visible through a gap between the buildings. The green sits at the center of a campus that was built over 270 years but planned, in its essential structure, within a single decade at the turn of the 20th century. The cannon, buried since 1840 and contested continuously since 1870, has outlasted every controversy, every renovation, and every administrative effort to rationalize student traditions into something more dignified. It is, in the end, more Princeton than Princeton itself."""

# ---------------------------------------------------------------------------
# Assembled POI data
# ---------------------------------------------------------------------------

PRINCETON_POIS: list[POIData] = [
    POIData(
        position=1,
        name="Nassau Hall",
        tagline="The Heart of Princeton · Est. 1756",
        lat=40.348600,
        lng=-74.659300,
        gps_radius_m=40,
        walk_note=None,
        categories=["History", "Architecture"],
        narrations=[
            NarrationData("snapshot", NASSAU_SNAPSHOT, 90),
            NarrationData("guide", NASSAU_GUIDE, 240),
            NarrationData("deepdive", NASSAU_DEEPDIVE, 600),
        ],
    ),
    POIData(
        position=2,
        name="Maclean House",
        tagline="The President's Residence · Since 1756",
        lat=40.349000,
        lng=-74.660300,
        gps_radius_m=30,
        walk_note="2 min from Nassau Hall",
        categories=["History", "Architecture"],
        narrations=[
            NarrationData("snapshot", MACLEAN_SNAPSHOT, 90),
            NarrationData("guide", MACLEAN_GUIDE, 240),
            NarrationData("deepdive", MACLEAN_DEEPDIVE, 600),
        ],
    ),
    POIData(
        position=3,
        name="Princeton University Art Museum",
        tagline="World-Class Collection · Free Entry",
        lat=40.347300,
        lng=-74.657600,
        gps_radius_m=35,
        walk_note="3 min southeast",
        categories=["Art", "Architecture"],
        narrations=[
            NarrationData("snapshot", ART_MUSEUM_SNAPSHOT, 90),
            NarrationData("guide", ART_MUSEUM_GUIDE, 240),
            NarrationData("deepdive", ART_MUSEUM_DEEPDIVE, 600),
        ],
    ),
    POIData(
        position=4,
        name="University Chapel",
        tagline="Third Largest University Chapel in the World",
        lat=40.348300,
        lng=-74.661400,
        gps_radius_m=35,
        walk_note="4 min west",
        categories=["Architecture", "History"],
        narrations=[
            NarrationData("snapshot", CHAPEL_SNAPSHOT, 90),
            NarrationData("guide", CHAPEL_GUIDE, 240),
            NarrationData("deepdive", CHAPEL_DEEPDIVE, 600),
        ],
    ),
    POIData(
        position=5,
        name="Blair Arch",
        tagline="Gothic Masterpiece · Most Photogenic Spot",
        lat=40.347600,
        lng=-74.660900,
        gps_radius_m=30,
        walk_note="3 min north",
        categories=["Architecture", "Student Life"],
        narrations=[
            NarrationData("snapshot", BLAIR_SNAPSHOT, 90),
            NarrationData("guide", BLAIR_GUIDE, 240),
            NarrationData("deepdive", BLAIR_DEEPDIVE, 600),
        ],
    ),
    POIData(
        position=6,
        name="Prospect House & Gardens",
        tagline="Woodrow Wilson's Former Home",
        lat=40.345100,
        lng=-74.657900,
        gps_radius_m=35,
        walk_note="5 min south on Prospect Ave",
        categories=["History", "Architecture"],
        narrations=[
            NarrationData("snapshot", PROSPECT_SNAPSHOT, 90),
            NarrationData("guide", PROSPECT_GUIDE, 240),
            NarrationData("deepdive", PROSPECT_DEEPDIVE, 600),
        ],
    ),
    POIData(
        position=7,
        name="Cannon Green",
        tagline="Home of Princeton's Most Stolen Object",
        lat=40.348100,
        lng=-74.659700,
        gps_radius_m=35,
        walk_note="5 min back north",
        categories=["History", "Student Life"],
        narrations=[
            NarrationData("snapshot", CANNON_SNAPSHOT, 90),
            NarrationData("guide", CANNON_GUIDE, 240),
            NarrationData("deepdive", CANNON_DEEPDIVE, 600),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Seed function
# ---------------------------------------------------------------------------


async def seed_database() -> None:
    """Seed the database with Princeton University tour data if not already seeded."""
    async with AsyncSessionLocal() as session:
        # Idempotency check: skip if Princeton already exists
        result = await session.execute(
            text("SELECT id FROM cities WHERE slug = 'princeton' LIMIT 1")
        )
        if result.scalar_one_or_none() is not None:
            logger.info("Seed: Princeton already exists — skipping.")
            return

        logger.info("Seed: Inserting Princeton University tour data...")

        # Insert city
        city_result = await session.execute(
            text(
                """
                INSERT INTO cities (name, slug, university, country, state, lat, lng, description, published)
                VALUES (:name, :slug, :university, :country, :state, :lat, :lng, :description, :published)
                RETURNING id
                """
            ),
            {
                "name": "Princeton",
                "slug": "princeton",
                "university": "Princeton University",
                "country": "US",
                "state": "NJ",
                "lat": 40.348200,
                "lng": -74.659300,
                "description": PRINCETON_DESCRIPTION,
                "published": True,
            },
        )
        city_id = city_result.scalar_one()
        logger.info("Seed: Inserted city id=%s", city_id)

        # Insert tour
        tour_result = await session.execute(
            text(
                """
                INSERT INTO tours (city_id, name, slug, tagline, duration_minutes, distance_meters,
                                   stop_count, categories, published)
                VALUES (:city_id, :name, :slug, :tagline, :duration_minutes, :distance_meters,
                        :stop_count, :categories, :published)
                RETURNING id
                """
            ),
            {
                "city_id": city_id,
                "name": "Historic Princeton Campus Walk",
                "slug": "historic-campus",
                "tagline": "270 years of history, science, and power — on foot",
                "duration_minutes": 75,
                "distance_meters": 2800,
                "stop_count": 7,
                "categories": ["History", "Architecture", "Student Life"],
                "published": True,
            },
        )
        tour_id = tour_result.scalar_one()
        logger.info("Seed: Inserted tour id=%s", tour_id)

        # Insert POIs and narrations
        for poi_data in PRINCETON_POIS:
            poi_result = await session.execute(
                text(
                    """
                    INSERT INTO pois (tour_id, position, name, tagline, lat, lng,
                                      gps_radius_m, walk_note, categories)
                    VALUES (:tour_id, :position, :name, :tagline, :lat, :lng,
                            :gps_radius_m, :walk_note, :categories)
                    RETURNING id
                    """
                ),
                {
                    "tour_id": tour_id,
                    "position": poi_data.position,
                    "name": poi_data.name,
                    "tagline": poi_data.tagline,
                    "lat": poi_data.lat,
                    "lng": poi_data.lng,
                    "gps_radius_m": poi_data.gps_radius_m,
                    "walk_note": poi_data.walk_note,
                    "categories": poi_data.categories,
                },
            )
            poi_id = poi_result.scalar_one()
            logger.info(
                "Seed: Inserted POI pos=%d name=%s id=%s",
                poi_data.position,
                poi_data.name,
                poi_id,
            )

            for narration in poi_data.narrations:
                await session.execute(
                    text(
                        """
                        INSERT INTO narrations (poi_id, depth_tier, script, duration_sec)
                        VALUES (:poi_id, :depth_tier, :script, :duration_sec)
                        """
                    ),
                    {
                        "poi_id": poi_id,
                        "depth_tier": narration.depth_tier,
                        "script": narration.script,
                        "duration_sec": narration.duration_sec,
                    },
                )

        await session.commit()
        logger.info("Seed: Princeton University tour data committed successfully.")
