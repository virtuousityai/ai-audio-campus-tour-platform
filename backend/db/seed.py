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


# ---------------------------------------------------------------------------
# University of Michigan POI data
# ---------------------------------------------------------------------------

UMICH_POIS: list[POIData] = [
    POIData(
        position=1, name="Michigan Stadium", tagline="Largest Stadium in the Western Hemisphere",
        lat=42.2659, lng=-83.7487, gps_radius_m=50, walk_note=None,
        categories=["Student Life", "History"],
        narrations=[
            NarrationData("snapshot", "Michigan Stadium holds 107,601 people — the largest in the Western Hemisphere. Built in 1927, it sits below street level so neighbors barely notice it. On game days, more people gather here than live in many American cities. The student tradition of standing for all four quarters, no matter the score, traces back to a 1922 reserve player named E. King Gill who stood ready to play if called. He never entered the game, but the gesture defined something essential about Michigan.", 90),
            NarrationData("guide", "Michigan Stadium — The Big House — holds 107,601 people, the largest in the Western Hemisphere. Built in 1927, architect Bernard Green made a distinctive choice: dig down rather than build up, so the stadium sits below street level. The original capacity was 72,000 and it has been expanded eight times since. The record attendance is 115,109, set in 2013. On fall Saturdays, more people gather here than live in cities like Providence, Rhode Island. What makes it different from any other stadium is the 12th Man tradition. In 1922, Coach Dana Bible ran out of healthy players mid-game. He called into the stands for E. King Gill, who suited up and stood ready on the sideline. He never played. But his willingness defined Aggie — sorry, Michigan — football culture. Today the entire student section stands for all four quarters, a living tribute to that moment. Gerald Ford played center here in the 1930s. Tom Brady quarterbacked here from 1995 to 1999. The fight song, 'The Victors,' written in 1898, was called the greatest fight song ever composed by John Philip Sousa himself.", 240),
            NarrationData("deepdive", "Michigan Stadium was completed in 1927 under the direction of Fielding Yost, Michigan's legendary athletic director who also coached the Wolverines to national championships. The below-grade design was intentional: the stadium is built into the ground, with only the rim visible from street level. This reduces wind, improves acoustics, and — critically — made it politically acceptable to neighborhood residents who didn't want a hulking structure looming over Ann Arbor. The foundation sits in Huron River floodplain soil, which required extraordinary engineering work in 1927 and again during the 2010-2015 renovation, a $485 million project by HKS Architects that added upper decks on both sides and luxury suites while preserving the bowl's fundamental character. The 12th Man tradition deserves its full story: E. King Gill was a student who had played for Michigan before transferring — records are incomplete — and Coach Bible called him down from the stands during a critical game. Gill stood for the remainder of the game in uniform. He never entered. He went on to become a petroleum engineer in Texas. Gerald Ford played center here from 1931 to 1934, was named the team's most valuable player in 1934, was offered contracts by the Detroit Lions and Green Bay Packers, turned both down to attend Yale Law School, and later said Michigan football taught him everything he needed to know about teamwork and leadership in public life. Tom Brady arrived at Michigan as a highly recruited quarterback but spent two seasons fighting for playing time, nearly transferred, then led Michigan to a Citrus Bowl victory in 1999. His journey here became a recurring motif in his later career story. The noise at The Big House during a sold-out game has been measured at over 130 decibels — comparable to a jet engine at close range. The bowl shape and below-grade design create an acoustic compression effect that amplifies crowd sound back onto the field.", 600),
        ],
    ),
    POIData(
        position=2, name="University of Michigan Museum of Art", tagline="World-Class Art · Free and Open to All",
        lat=42.2731, lng=-83.7378, gps_radius_m=30, walk_note="15 min walk northeast from Michigan Stadium",
        categories=["Art", "Architecture"],
        narrations=[
            NarrationData("snapshot", "One of the finest university art museums in North America — and it's free. UMMA holds over 23,000 works spanning 5,000 years: Old Masters, Chinese bronzes, African objects, American modernists. The 2009 expansion by Allied Works Architecture created a dramatic atrium that floods the galleries with natural light. Walk in off the street and you're standing in front of a Picasso. That's Michigan.", 90),
            NarrationData("guide", "The University of Michigan Museum of Art was founded in 1856, making it one of the oldest university art museums in the country. The collection has grown to over 23,000 works across 5,000 years of human creativity. The museum is anchored in Alumni Memorial Hall, completed in 1910, and dramatically expanded in 2009 with a new wing by Allied Works Architecture of Portland. The expansion created a soaring entrance atrium that floods into the older gallery spaces, bringing natural light into rooms that had been poorly lit for decades. The collection's highlights include significant Picasso prints and paintings, a remarkable set of Chinese bronzes from the Han and Tang dynasties, Old Master drawings including Rembrandt etchings, and a strong collection of American modernists — Winslow Homer, Thomas Eakins, Georgia O'Keeffe. Admission has always been free, by design. The philosophy, embedded since 1856, is that great art belongs to everyone. Annual attendance runs around 100,000. The museum serves as an active teaching resource for Michigan students across disciplines — not just art history, but chemistry students analyzing pigments, engineering students studying structural techniques, medical students using art to train visual diagnosis.", 240),
            NarrationData("deepdive", "Michigan's art museum was established in 1856 under university president Henry Philip Tappan, who had studied in Berlin and was determined to give Michigan the cultural institutions of a European research university. The founding collection was modest — plaster casts, engravings, some paintings donated by alumni — but it established the principle that a great university needed a great museum. Alumni Memorial Hall was built in 1910 in Beaux-Arts style as a memorial to Michigan alumni who died in the Civil War and Spanish-American War. The 2009 Allied Works expansion was controversial when proposed: critics worried a bold contemporary addition would clash with the 1910 building. The architects chose to connect the buildings with a glass and steel atrium that serves as a neutral mediator between the historical and the contemporary. The atrium has become one of the most admired spaces in the Midwest. The Chinese bronze collection is particularly significant — the Tang Dynasty horses are considered among the finest examples outside China, and the Han Dynasty ritual bronzes date to the 2nd century BCE. The museum acquired many of these pieces in the early 20th century when American universities were building Asian art collections aggressively. The Picasso collection spans his career from Blue Period works to late prints. Specific pieces include a rare 1906 gouache from the period just before Cubism and a significant set of Vollard Suite etchings. The museum's relationship to Detroit's cultural ecosystem is worth noting: it sits between the Detroit Institute of Arts — one of the great encyclopedic museums in the country — and the more specialized galleries emerging in the city, giving Michigan students access to a remarkably rich visual arts environment within 45 minutes.", 600),
        ],
    ),
    POIData(
        position=3, name="Burton Memorial Tower", tagline="Michigan's Carillon Tower · 10-Story Gothic Landmark",
        lat=42.2782, lng=-83.7389, gps_radius_m=30, walk_note="8 min walk north from UMMA",
        categories=["Architecture", "History"],
        narrations=[
            NarrationData("snapshot", "Burton Tower rises 10 stories above central campus and contains 53 carillon bells — the largest weighing 12 tons, cast in Belgium. You can hear it across all of Ann Arbor at noon and 5pm. Designed by Albert Kahn, the most important industrial architect in American history, it was named for Marion Leroy Burton, the Michigan president who envisioned a university that could compete with the Ivy League.", 90),
            NarrationData("guide", "Burton Memorial Tower was completed in 1936, designed by Albert Kahn — the Detroit architect whose industrial buildings defined American manufacturing in the 20th century. Kahn designed the Ford River Rouge Complex, the General Motors Building, and dozens of Detroit's most important structures. For Michigan, he designed in Collegiate Gothic, matching the style established elsewhere on campus. The tower rises 10 stories and houses the Charles Baird Carillon: 53 bells cast at the Petit & Fritsen foundry in the Netherlands, the largest bell weighing 12 tons. The carillon plays daily at noon and 5pm, and university carillonists give regular concerts, particularly on evenings in spring and fall. You can climb to the observation deck on Sunday afternoons for a panoramic view of campus and the city. The tower was named for Marion Leroy Burton, Michigan's president from 1920 to 1925. Burton arrived with a vision: transform Michigan from a respected regional school into a genuine peer of the great research universities. He launched massive campus expansion, hired major faculty, and built the hospital complex. He died in office in 1925, at 50 years old, before his vision was complete. The tower was built to honor him.", 240),
            NarrationData("deepdive", "Albert Kahn deserves more time than this stop allows, but here is the outline: he was born in Germany in 1869, immigrated to Detroit at age 11, apprenticed as a draftsman, and by 1900 had established the firm that would design the infrastructure of American industrial capitalism. The Ford Highland Park plant (1909) introduced the moving assembly line. The Ford River Rouge Complex (1917-1928) was the largest industrial complex in the world. He designed 1,000 buildings for the Soviet Union's industrialization program in the 1930s. At the same time, he was designing Collegiate Gothic buildings for the University of Michigan — an apparent contradiction that he saw as no contradiction at all. For Kahn, buildings were problems to solve, and the problem of a campus tower was: how do you make something that will anchor this space for a century? The carillon bells were selected through a process that took years. Charles Baird, Michigan's first athletic director (1898-1909), had established the tradition of Michigan athletic success that culminated in The Big House. His name on the carillon connects two of Michigan's most distinctive institutions. The bell-founding tradition at Petit & Fritsen dates to the 17th century; each bell is tuned by shaving metal from the inside to achieve precise pitch. The 53-bell range allows performance of virtually any Western music composed for carillon. The observation deck view from Burton Tower reveals the campus plan: you can see how Kahn and his predecessors laid out the central campus in a rough grid, with the Medical Campus to the north, the athletic campus to the south, and the Diag as the connective tissue.", 600),
        ],
    ),
    POIData(
        position=4, name="Angell Hall", tagline="Michigan's Academic Heart · Home of LSA",
        lat=42.2773, lng=-83.7381, gps_radius_m=30, walk_note="3 min walk from Burton Tower",
        categories=["Architecture", "History"],
        narrations=[
            NarrationData("snapshot", "Angell Hall anchors the College of Literature, Science, and the Arts — Michigan's largest college, 18,000 students, 100 departments. The Greek Revival columns face South University. Inside, a long corridor called the Fishbowl has been a student gathering point for a century. Gerald Ford organized early political campaigns here. The observatory across the street has a telescope from 1854 still in use.", 90),
            NarrationData("guide", "Angell Hall was completed in 1924, designed by Albert Kahn in Greek Revival style to anchor Michigan's growing academic campus. It was named for James Burrill Angell, Michigan's president from 1871 to 1909 — the longest tenure in the university's history. Angell presided over Michigan's transformation from a small state college into a major research university, and found time to serve as US Minister to China and Turkey during his presidency, the only university president ever recalled by the US government to serve as a diplomat twice while remaining in office. The building's Parthenon-like columns face South University Avenue. Inside, the famous Fishbowl — a long central corridor visible through large windows from outside — has been a student gathering point, protest staging ground, and political forum for 100 years. Gerald Ford organized his first successful political campaign here in 1948 when he ran for Congress. The building houses the central administrative offices of LSA, the largest college at Michigan, with 18,000 undergraduates and over 100 departments. The Detroit Observatory, built in 1854 on Observatory Hill across the street, houses a Fitz refractor telescope that remains in active use and is one of the oldest working research telescopes in the country.", 240),
            NarrationData("deepdive", "James Burrill Angell's presidency from 1871 to 1909 is one of the most remarkable in American higher education. He arrived when Michigan was a solid regional school and left it as a genuine research university with an international reputation. His diplomatic interruptions are worth dwelling on: in 1880, President Hayes asked Angell to negotiate a new treaty with China governing immigration — the Angell Treaty of 1880, which modified the Burlingame Treaty and is still studied in diplomatic history. He went to China, negotiated the treaty, and returned to Michigan. In 1897, President McKinley asked him to serve as Minister to Turkey, during the period of the Hamidian massacres and the Armenian crisis. He went, served, and returned to Michigan. He considered both interruptions duties he couldn't decline. The Greek Revival architectural choice for Angell Hall in 1924 was deliberate: Kahn was designing in a style that connected Michigan to classical learning traditions, contrasting with the more utilitarian buildings of the engineering campus. The Fishbowl has been the site of specific historical moments: the teach-in of March 1965, organized by faculty, was the first Vietnam War teach-in in American history — a model that spread to hundreds of campuses within months. The Black Action Movement student strike of 1970 began with organizing in the Fishbowl. The shantytown protest against South African apartheid in 1985 was staged on the Diag visible from Fishbowl windows. LSA's scope today — 18,000 undergraduates, 100+ departments, more than the entire enrollment of many American universities — makes it one of the most complex administrative units in American higher education.", 600),
        ],
    ),
    POIData(
        position=5, name="Law Quadrangle", tagline="Oxford in Michigan · The Most Beautiful Law School in America",
        lat=42.2751, lng=-83.7403, gps_radius_m=35, walk_note="5 min walk southwest from Angell Hall",
        categories=["Architecture", "History"],
        narrations=[
            NarrationData("snapshot", "The Law Quad is called the most beautiful law school campus in America — and it's hard to argue. Built 1923-1933 with a $7 million gift from one alumnus who wanted to replicate Oxford, it's a complete Collegiate Gothic complex: four connected buildings enclosing a cloistered courtyard where the sounds of Ann Arbor disappear. Walk into the cloister. Stand there for a moment. It works.", 90),
            NarrationData("guide", "The Law Quadrangle was built between 1923 and 1933 with an extraordinary $7 million gift from William Wilson Cook, a Michigan Law alumnus who made his fortune in New York corporate law. Cook had a specific vision: replicate Oxford and Cambridge for Michigan students. He hired York and Sawyer, architects who had designed major Gothic buildings in New York, and told them to build something that would last centuries. The four buildings — Hutchins Hall, the Legal Research Library, the Cook Dormitory, and the Lawyers Club — enclose a cloistered courtyard that is architecturally complete. The Legal Research Library's reading room has a fan-vaulted ceiling modeled directly on Henry VII's Chapel in Westminster Abbey. Step inside and look up. The stone carving was done by craftsmen brought from England. Cook donated so obsessively to Michigan Law that the complex was sometimes called Cook's Monument. He is buried in a small chapel within the Lawyers Club building — he never married, had no children, and made Michigan his legacy. Walk through the cloister. The city sounds stop. It's one of the great architectural experiences in the Midwest.", 240),
            NarrationData("deepdive", "William Wilson Cook graduated from Michigan Law in 1882, moved to New York, and built a career at Sullivan & Cromwell — one of the great corporate law firms of the Gilded Age. He made a fortune representing railroads and trusts. He also accumulated a profound, almost bitter, envy of Harvard and Yale alumni who dominated the New York bar and corporate boardrooms. Cook decided to give his wealth to Michigan specifically to prove that a public university could build institutions as beautiful and as serious as anything in the Ivy League. The $7 million he donated in the 1920s is equivalent to roughly $120 million today. He specified Oxford and Cambridge as models — specifically Christ Church Meadow and Magdalen College as architectural references. York and Sawyer traveled to England, photographed the models, and designed buildings that are faithful to the Gothic tradition without being slavish copies. The Legal Research Library fan vault is a particular achievement: Henry VII's Chapel at Westminster (completed 1512) has the most elaborate fan vaulting in England. Michigan's version, executed in Indiana limestone rather than English Purbeck marble, achieves a similar effect through careful proportioning. Cook himself reviewed the work obsessively — he visited the construction site repeatedly, criticized details, and died in 1930 before the complex was complete. His ashes were interred in the Lawyers Club chapel, as he had specified. Michigan Law has ranked consistently in the top 10 American law schools for decades. Notable alumni include Supreme Court Justice John Paul Stevens, who graduated in 1947. The quadrangle is used for filming regularly — its Gothic completeness is genuinely rare in North America.", 600),
        ],
    ),
    POIData(
        position=6, name="The Diag", tagline="Campus Crossroads · Heart of Michigan Student Life",
        lat=42.2770, lng=-83.7374, gps_radius_m=40, walk_note="3 min walk northeast from Law Quad",
        categories=["Student Life", "History"],
        narrations=[
            NarrationData("snapshot", "The Diag is Michigan's central lawn, cut by diagonal paths — hence the name. An M is embedded in the pavement at the center. Step on it before your first exam and you'll fail. Step on it after your first exam and your luck is sealed for four years. On October 14, 1960, at 2am, JFK stood near here and proposed, off the cuff, a national program of young Americans serving overseas. Four months later, the Peace Corps existed.", 90),
            NarrationData("guide", "The Diag is the open lawn at the center of Michigan's original campus, formed by diagonal paths cutting across the university's founding square. The Michigan M embedded at the center carries a two-part superstition: step on it before your first blue book exam and you'll fail; step on it after your first exam and your Michigan luck is set for four years. Freshmen learn this during orientation. Upperclassmen enforce it socially. The superstition has persisted for at least 80 years with no known origin point. The Diag has been the site of Michigan's most consequential public moments. On the evening of October 14, 1960, presidential candidate John F. Kennedy arrived in Ann Arbor from a debate, exhausted. Ten thousand students had gathered — at 2am — near the Michigan Union steps, adjacent to the Diag. Kennedy had no prepared remarks. He spoke extemporaneously about young Americans, education, and service abroad. He asked the crowd how many would be willing to serve their country overseas. The crowd roared. Sargent Shriver, watching from the crowd, took notes. The Peace Corps was established by executive order four months later.", 240),
            NarrationData("deepdive", "The October 14, 1960 Kennedy speech deserves its full story. Kennedy was in the middle of a grueling campaign, behind in some polls, exhausted from a presidential debate earlier that day. His motorcade arrived in Ann Arbor at 2am. The student organizers — members of the Michigan student government — had publicized the visit aggressively. Ten thousand students showed up at 2am on a Tuesday. Kennedy spoke for less than five minutes. He did not use the phrase 'Peace Corps' — the name came later. He asked a series of questions: How many of you are willing to spend two years in Ghana? How many in Turkey? How many are willing to work in a village? The crowd's response electrified him. He told aides afterward that he had never felt that kind of energy from an audience. Sargent Shriver, who was in the crowd and who would become the Peace Corps' first director, later said the speech gave him the mandate he needed to push the idea through Washington's bureaucracy. Kennedy signed the executive order creating the Peace Corps on March 1, 1961 — 137 days after Ann Arbor. A plaque on the Michigan Union steps marks the spot. Michigan has been one of the largest sending schools for Peace Corps volunteers since 1961. The Diag itself has witnessed 150 years of American political history: the first Vietnam War teach-in in 1965, organized by faculty in the buildings surrounding the Diag; the Black Action Movement strike of 1970; the anti-apartheid shantytown of 1985; the inaugural Earth Day in 1970, which was itself proposed by Michigan Senator Gaylord Nelson and had one of its largest events here. The M in the pavement dates to at least the 1940s — earlier versions existed, repeatedly repainted.", 600),
        ],
    ),
    POIData(
        position=7, name="Michigan Union", tagline="Where JFK Launched the Peace Corps · Student Hub Since 1919",
        lat=42.2745, lng=-83.7393, gps_radius_m=30, walk_note="3 min walk south from The Diag",
        categories=["History", "Student Life"],
        narrations=[
            NarrationData("snapshot", "The Michigan Union has been the center of student life since 1919. It's most famous for one moment: October 14, 1960, at 2am, when JFK stood on the front steps and proposed a national service program for young Americans. The Peace Corps was born at this spot. A plaque on the front steps marks it.", 90),
            NarrationData("guide", "The Michigan Union was completed in 1919 as a student gathering place, and remains that today — dining, meeting rooms, student organizations, and event spaces fill the building. Its Collegiate Renaissance architecture stands in contrast to the Gothic elsewhere on campus. But the Union is defined by one moment: October 14, 1960. John F. Kennedy arrived at 2am, exhausted from a campaign appearance. Ten thousand students were waiting. He had no prepared remarks. Standing near these front steps, he extemporaneously proposed a new program — young Americans serving abroad, using their education for peace rather than war. The crowd responded with overwhelming enthusiasm. The Peace Corps was established by executive order on March 1, 1961. Michigan has sent more Peace Corps volunteers than almost any other university. A plaque on the front steps marks the exact spot. The Union also has a historical footnote for women's rights: through the 1950s, women were not allowed to enter through the front door. They used a side entrance. The policy ended as Michigan began coeducating its campus culture in the 1960s.", 240),
            NarrationData("deepdive", "The October 14, 1960 event at the Michigan Union is one of the best-documented impromptu speeches in American political history, because so many people were there and wrote about it afterward. Kennedy's motorcade arrived at 2am from Detroit, where he had appeared earlier that evening. The Ann Arbor stop was late and unplanned as a major event. Student organizers Tom Hayden — later a prominent antiwar activist and California state senator — and Al Haber had organized the gathering, expecting a few hundred people. Ten thousand came. Kennedy stepped onto the Union steps. He spoke without notes. He asked how many students would serve two years in Africa, Latin America, Asia. He said: 'On your willingness to contribute part of your life to this country I think will depend the answer whether a free society can compete.' Sargent Shriver, who became Peace Corps director, later said: 'The students' response that night told me we could recruit the volunteers we'd need.' The Peace Corps Act was signed on September 22, 1961. By the end of 1961, 124 volunteers were serving in Ghana and Tanzania. Today the agency has placed 240,000 volunteers in 141 countries. Michigan has consistently been among the top 10 sending schools. Tom Hayden later wrote that the Michigan Union speech was the moment he understood that a new generation was ready to take political responsibility. Hayden himself went on to help found Students for a Democratic Society, whose founding manifesto — the Port Huron Statement — was drafted at a United Auto Workers retreat near Port Huron, Michigan, in 1962. Michigan was the epicenter of 1960s American student political organization.", 600),
        ],
    ),
    POIData(
        position=8, name="Nichols Arboretum", tagline="170 Acres of Living Science · The Arb",
        lat=42.2812, lng=-83.7268, gps_radius_m=50, walk_note="15 min walk east",
        categories=["Nature", "History"],
        narrations=[
            NarrationData("snapshot", "The Arb is 170 acres of natural landscape along the Huron River — trails, native trees, and one of the largest historic peony collections in North America. Michigan students come here during exam periods to think. Alumni return here. It's been a teaching laboratory for botany and ecology since 1907, and one of the best things about Ann Arbor that nobody outside the university knows about.", 90),
            NarrationData("guide", "The Nichols Arboretum was established in 1907 on Huron River land at the edge of campus, funded initially by the university and endowed by a 1920 bequest from Walter Nichols, a Detroit businessman. Its 170 acres contain over 5,000 species of trees, shrubs, and perennials, arranged both for scientific study and public enjoyment. The arboretum is managed by the School for Environment and Sustainability and serves as an outdoor laboratory for ecology, botany, landscape architecture, and environmental science courses. The peony collection, planted in the 1920s on a south-facing hillside above the Huron, contains 250 varieties and is one of the most significant historic collections in North America. It blooms in late May and early June and draws visitors from across Michigan. The trails through the Arb connect to the broader Huron River Greenway, a 104-mile network of paths along the river. Generations of Michigan students have walked these trails during finals periods. There is research suggesting that natural environments measurably reduce cortisol levels and improve cognitive performance under stress — the Arb has been a living experiment in this phenomenon for a century.", 240),
            NarrationData("deepdive", "The Arb's founding in 1907 was part of a broader movement in American universities to establish outdoor laboratories — spaces where biological and ecological science could be practiced in the field rather than just the classroom. Michigan was an early leader in this movement, reflecting the university's land-grant sensibility even though Michigan predates the Morrill Act (1862) that created land-grant universities. Walter Nichols' 1920 bequest provided the endowment that secured the arboretum's future. Nichols was a Detroit businessman with no scientific training who had simply come to love the place during walks from his Ann Arbor home. His bequest is a common pattern in the history of American conservation: non-scientists who became passionate advocates for specific landscapes. The peony collection's history is particularly interesting. In the 1920s, American horticultural institutions were actively corresponding with European and East Asian nurseries to build comprehensive collections of species that had been cultivated for centuries. The arboretum's collection includes Chinese tree peonies (Paeonia suffruticosa) with cultivar histories going back to the Tang Dynasty and European herbaceous peonies with unbroken lineages to 17th-century French and Dutch gardens. The arboretum's connection to the School for Environment and Sustainability (SEAS) has become increasingly important as climate change research has intensified. The arboretum maintains long-term phenological records — when species bloom, when leaves turn, when birds arrive — that have become valuable climate data sets. Some records go back to 1907. Comparing them to current observations reveals measurable changes in seasonal timing. The arboretum during COVID lockdowns in 2020 became one of the few places Ann Arbor residents could go. Attendance records from that period show that access to natural spaces during crisis is not a luxury but a public health necessity.", 600),
        ],
    ),
]

# ---------------------------------------------------------------------------
# Texas A&M POI data
# ---------------------------------------------------------------------------

TAMU_POIS: list[POIData] = [
    POIData(
        position=1, name="Kyle Field", tagline="Home of the 12th Man · 102,733 Seat Cathedral",
        lat=30.6100, lng=-96.3408, gps_radius_m=50, walk_note=None,
        categories=["Student Life", "History"],
        narrations=[
            NarrationData("snapshot", "Kyle Field holds 102,733 people — one of the largest stadiums in the world. But the number isn't what defines it. What defines Kyle Field is the 12th Man: the tradition of all 102,000 fans standing throughout the entire game, ready to play if needed. It traces to 1922, when a student named E. King Gill stood on the sideline ready to play if called. He never entered. The tradition has never stopped.", 90),
            NarrationData("guide", "Kyle Field has been home to Texas A&M football since 1904. The current capacity of 102,733 was reached after a $485 million renovation completed in 2015, which added upper decks on both sides and transformed the stadium into a football-specific venue. The renovation was designed by HKS Architects, who also designed AT&T Stadium in Dallas. What distinguishes Kyle Field from every other stadium in America is the 12th Man tradition. In 1922, during a critical game, Coach Dana Bible called into the stands for E. King Gill, a student who had previously played football. Gill suited up and stood on the sideline for the remainder of the game, ready to play if called. He was never needed. But the gesture — one student willing to give everything for Texas A&M — became the defining expression of Aggie identity. Today, the entire student section stands for all four quarters of every home game. No sitting, no matter the score. The noise at Kyle Field is legendary: the crowd roar has been measured at levels comparable to a jet engine. Texas A&M trademarked the term '12th Man' and has had legal battles with NFL teams who adopted the phrase.", 240),
            NarrationData("deepdive", "Kyle Field's history begins with a wooden grandstand in 1904 and has been a continuous story of expansion driven by the growth of Aggie football's cultural significance. The 2015 renovation was the most dramatic: architect HKS designed cantilevered upper decks on both the east and west sides, creating a bowl that traps sound and amplifies crowd noise to extraordinary levels. The acoustic engineering was intentional — the upper decks angle inward to direct crowd noise toward the field. Measurements during peak games have recorded crowd noise exceeding 110 decibels sustained over several seconds. E. King Gill's story is well-documented: he was a freshman who had played briefly for A&M before moving to the basketball team. On January 2, 1922, during the Dixie Classic in Dallas, Coach Dana Bible found himself with only 11 healthy players after injuries. Gill came from the stands, suited up in a spare uniform, and stood ready. A&M won. Gill later became a petroleum engineer, married, raised a family in Texas, and lived to see his gesture become a founding myth. He died in 1958. The 12th Man trademark issue is significant: Texas A&M registered the term in 1990. The Seattle Seahawks adopted 12th Man imagery in 2004. Texas A&M sued. The settlement in 2006 required the Seahawks to pay a licensing fee and acknowledge A&M's ownership of the trademark — an unusual case of a university holding intellectual property rights over a sports marketing term used by an NFL franchise. Game day at Kyle Field is worth describing in full: Midnight Yell Practice the night before, held inside the stadium with 50,000 students; the Corps of Cadets march on game morning; the Aggie War Hymn played by the band; the specific traditions of the student section including hand signals, yell leaders, and synchronized responses to game events. The economic impact of a single home game on College Station is estimated at $8-12 million.", 600),
        ],
    ),
    POIData(
        position=2, name="Academic Building", tagline="The Heart of Campus · Tower of Learning",
        lat=30.6185, lng=-96.3371, gps_radius_m=30, walk_note="15 min walk north from Kyle Field",
        categories=["Architecture", "History"],
        narrations=[
            NarrationData("snapshot", "The Academic Building is Texas A&M's symbolic center — its domed cupola and clock tower have anchored campus since 1914. Classic Revival columns signal that A&M's practical mission — agriculture, engineering — is as intellectually serious as any liberal arts college. Every graduation ceremony has a moment here. The Academic Plaza surrounding it is where A&M's most sacred traditions take place.", 90),
            NarrationData("guide", "The Academic Building was completed in 1914 as the administrative heart of Texas A&M. Its Classic Revival architecture — columns, dome, formal symmetry — was a deliberate statement: this practical school, founded to teach agriculture and engineering to Texas farm boys, deserved the same physical dignity as any liberal arts institution. The dome and clock tower are the most photographed elements of A&M and appear on virtually every piece of official university imagery. The building housed the president's office for decades and remains the administrative center of the university. The Academic Plaza surrounding it is the site of A&M's most solemn traditions. Silver Taps, held the first Tuesday of each month when an A&M student has died, brings thousands of students to the plaza in silence. The Ross Volunteers fire a 21-gun salute. The lights go out. A bugler plays taps. Students stand in the dark and then disperse without speaking. The tradition has continued since 1898.", 240),
            NarrationData("deepdive", "Texas A&M was founded in 1876 as the Agricultural and Mechanical College of Texas — the state's first public institution of higher education under the Morrill Act. The founding was politically contentious: supporters of the University of Texas, founded seven years later in 1883, saw A&M as a rival for state funding. The tension between the two institutions has defined Texas higher education ever since. A&M's original mission was exclusively practical: agriculture, engineering, military training for men. No women, no liberal arts, no law or medicine. The Academic Building's Classic Revival style in 1914 was itself a statement of ambition — a deliberate attempt to claim intellectual legitimacy through architectural language. The architect was Frederick Giesecke, A&M's own professor of engineering and architecture, who had studied at MIT. The building's dome and clock tower have been modified several times; the current appearance dates largely to a 1930s renovation. Silver Taps deserves its full story: the tradition began in 1898 when students spontaneously gathered after a classmate died suddenly. Over time it formalized into its current precise ritual. The Ross Volunteers — the elite honor guard of the Corps of Cadets — fire the salute. The Singing Cadets may sing. Students receive notification through a silver taps announcement that gives only initials and class year, preserving privacy. The tradition of gathering in silence, standing in the dark, dispersing without speaking — these choreographed elements of grief are powerful precisely because they are collective and non-verbal. A&M students who experience Silver Taps describe it as one of the defining experiences of their time on campus.", 600),
        ],
    ),
    POIData(
        position=3, name="Century Tree", tagline="Oldest Tree on Campus · Aggie Romance Legend",
        lat=30.6176, lng=-96.3374, gps_radius_m=25, walk_note="2 min walk from Academic Building",
        categories=["Student Life", "History"],
        narrations=[
            NarrationData("snapshot", "The Century Tree is a massive live oak near the Academic Building. Walk under it with your significant other and you will marry them. Walk under it alone and you will be forever single. Aggies treat this with complete seriousness. Couples make pilgrimages. People cross the street to avoid it when alone. A lightning strike nearly killed the tree in the 1990s — arborists worked for years to save it.", 90),
            NarrationData("guide", "The Century Tree is a southern live oak standing near the Academic Building that has become the center of one of A&M's most beloved romantic traditions. Walk under the tree's canopy with a romantic partner and you will marry that person. Walk under it alone and you will be forever single. The tradition is taken seriously — not with superstition exactly, but with the kind of affectionate seriousness that makes campus legends persist. Couples who have walked under the Century Tree have returned to get engaged beneath it. Alumni bring their children to walk under it. People genuinely cross the street rather than walk under it alone. The tree was struck by lightning in the 1990s and was in danger of dying. The university's arborists launched an intensive multi-year treatment: soil aeration, root stimulation, careful pruning, and close monitoring. The tree recovered fully. The recovery itself became part of the tree's story — proof that the campus would fight to preserve it.", 240),
            NarrationData("deepdive", "Southern live oaks (Quercus virginiana) are iconic trees of the American South and Gulf Coast. They are evergreen, which is unusual for oaks in North America — they hold their leaves through winter, replacing them in early spring in a brief period called the spring leaf exchange. They grow to massive size — canopy spreads of 60 to 100 feet are common in mature specimens — and can live for several centuries. The specific age of the Century Tree is disputed; the name suggests 100 years, but dendrochronological analysis (counting growth rings, which requires a core sample) would be needed to establish it precisely. University arborists have estimated ages ranging from 80 to over 100 years, depending on methods used. The romantic tradition has no documented origin point — it appears in student oral tradition at least as far back as the 1950s and probably earlier. Similar traditions exist at other universities (the Sycamore Tree at Penn State, various 'kissing trees' and gates at campuses across the country), suggesting a broader cultural pattern of campus landscapes becoming sites of romantic ritual. What makes the Century Tree tradition distinctive is its specificity and its dual nature: both a blessing (walk with someone, marry them) and a curse (walk alone, remain so). The lightning strike of the 1990s was treated by the university as a genuine crisis. The arboricultural response involved soil decompaction using compressed air, installation of supplemental irrigation, removal of competing vegetation from the root zone, and careful crown reduction to reduce wind loading. The response was more intensive than might be expected for a single tree, reflecting the tree's cultural significance to the institution.", 600),
        ],
    ),
    POIData(
        position=4, name="Rudder Tower", tagline="Named for a Hero · D-Day's Pointe du Hoc",
        lat=30.6159, lng=-96.3378, gps_radius_m=30, walk_note="3 min walk south from Century Tree",
        categories=["History", "Architecture"],
        narrations=[
            NarrationData("snapshot", "Rudder Tower is named for James Earl Rudder, who led the Ranger assault on Pointe du Hoc on D-Day — scaling 100-foot cliffs under fire to destroy German guns threatening the Normandy landings. Of 225 Rangers who started, 90 survived. Rudder was wounded twice. He later came back to Texas A&M as president and opened the university to women and African Americans, transforming it from a military college into a research university.", 90),
            NarrationData("guide", "Rudder Tower was completed in 1971 and named for James Earl Rudder, the most decorated Texan of World War II. On D-Day, June 6, 1944, Colonel Rudder led the 2nd Ranger Battalion in the assault on Pointe du Hoc — the clifftop battery between Omaha and Utah beaches whose 155mm guns threatened both landing zones. The Rangers scaled 100-foot cliffs using ropes and ladders under withering German fire. Of the 225 Rangers who began the assault, 90 survived. Rudder was wounded twice during the battle. The Pointe du Hoc battery was silenced and the flanks of Omaha Beach secured. Rudder returned to Texas A&M as president in 1959 and served until his death in 1970. His presidency was as consequential as his military service: he admitted women and African American students, ended the mandatory Corps of Cadets requirement, launched the research mission that made A&M a flagship university, and enrolled A&M in the Southeastern Conference. He transformed a military agricultural college into a modern research university while preserving the traditions that defined Aggie identity.", 240),
            NarrationData("deepdive", "Pointe du Hoc is one of the most documented tactical operations in military history, and Rudder's role in it is central. The German battery at Pointe du Hoc was considered by Allied planners to be the most dangerous single target on the Normandy coast: six 155mm guns in concrete casemates, positioned to fire on both Omaha Beach (to the east) and Utah Beach (to the west), with ranges that covered the entire invasion fleet. Conventional bombing had failed to destroy the guns. The decision was made to send Rangers to scale the cliffs and destroy them by hand. Rudder commanded the operation personally — a decision that General Omar Bradley later said was extraordinary, because commanders of his rank were not expected to lead assaults personally. The cliffs were 85 to 100 feet of sheer chalk. The Rangers used rocket-propelled grappling hooks and ladders. German defenders cut the ropes from above. Rangers climbed hand-over-hand up the remaining ropes while being shot at. Rudder reached the top with the first wave. He established a command post in a shell crater, was wounded in the leg, continued directing the battle. A second German counterattack nearly overran the Ranger position. Of 225 Rangers who began, 90 were combat-effective by the end of D-Day. The guns were found — moved from their casemates to avoid bombing, hidden in an orchard nearby — and destroyed with thermite grenades by two Rangers acting on their own initiative. Rudder's presidency of A&M (1959-1970) was equally consequential. The mandatory Corps requirement was eliminated in 1965 after enrollment had stagnated for a decade — other Texas universities were growing while A&M, restricted to military men, could not compete. Rudder argued that A&M's traditions were strong enough to survive becoming a civilian university. He was right: the Corps continued, voluntarily, and A&M enrollment more than doubled within a decade of the change.", 600),
        ],
    ),
    POIData(
        position=5, name="Memorial Student Center", tagline="A Living Memorial · Texas A&M's Cultural Heart",
        lat=30.6148, lng=-96.3387, gps_radius_m=35, walk_note="3 min walk south from Rudder Tower",
        categories=["History", "Student Life"],
        narrations=[
            NarrationData("snapshot", "The MSC is dedicated to Aggies who died in service to their country — more Texas A&M graduates served in World War II than from any other university. You remove your hat entering the building, as you would in a church or at a grave. You don't sit on the steps. Inside: galleries, dining, and one of the finest collections of American and Texas art on any campus.", 90),
            NarrationData("guide", "The Memorial Student Center was dedicated in 1950 to Aggies who gave their lives in World War II. More Texas A&M graduates served in the war — 14,000 — than from any other American university. Nine hundred died. The MSC stands as their memorial. The building's traditions reflect this: you remove your hat or cap upon entering, as you would entering a church or standing at a grave. You do not sit on the MSC steps — they are not a place to lounge. The building has been expanded several times and now houses galleries, dining facilities, the largest event spaces on campus, and student programming organizations. The Wiatt Gallery contains important collections of American modernist and Texas landscape painting. The MSC Committees — student organizations that report to the MSC — manage dozens of programs: performing arts, political speakers, visual art, film, international cultural programs. The MSC is one of the most active student programming organizations in the country.", 240),
            NarrationData("deepdive", "Texas A&M's World War II service record is extraordinary. Of the approximately 14,000 A&M graduates who served, the university produced more officers than any other school in the country — more than West Point, Annapolis, or any Ivy League university. This reflects A&M's mandatory Corps of Cadets: every male student who enrolled between 1876 and 1965 received ROTC training and graduated with a military commission available. By 1941, A&M had been producing commissioned officers for 65 years. The 900 who died included seven general officers. Among the most decorated: Doris Miller, the first African American to receive the Navy Cross, was not an A&M graduate — but the broader point stands that Texas produced an extraordinary proportion of American military leadership in the war. The decision after the war to make the student union a memorial rather than a recreation center was deliberate and has shaped A&M's campus culture ever since. The hat tradition extends to not wearing the Aggie Ring (the distinctive Texas A&M class ring) while in certain contexts — there is an elaborate ritual culture around the ring, including a Ring Dunk ceremony. The MSC art collection was assembled primarily through the MSC's Visual Arts Committee, which began acquiring works in the 1950s and has built a collection valued at tens of millions of dollars. The Texas landscape painting tradition represented in the collection includes works by Porfirio Salinas, known as 'the Bluebonnet Painter,' and members of the Dallas Nine, the regionalist movement that documented Texas landscapes in the mid-20th century. The MSC's programming scope — bringing major performing artists, political figures, and international cultural programs to College Station — reflects the MSC's founding vision that a memorial to the fallen should honor them by making culture and learning accessible to the living.", 600),
        ],
    ),
    POIData(
        position=6, name="Simpson Drill Field", tagline="Where the Corps Marches · Heart of Military Tradition",
        lat=30.6170, lng=-96.3400, gps_radius_m=40, walk_note="3 min walk west",
        categories=["History", "Student Life"],
        narrations=[
            NarrationData("snapshot", "Simpson Drill Field is the parade ground for the Corps of Cadets — the largest ROTC program outside the military academies, with 2,000 students. Texas A&M was founded as a military college in 1876. The Corps was mandatory until 1965. On football Saturdays, the entire Corps marches in formation to Kyle Field — one of the great spectacles in college sports.", 90),
            NarrationData("guide", "Simpson Drill Field is the formal parade ground for the Corps of Cadets, the military organization that was the entire student body of Texas A&M from 1876 until 1965, when civilian enrollment was first permitted. Today about 2,000 students are in the Corps voluntarily — the largest ROTC program outside West Point, Annapolis, and the Air Force Academy. The Corps has produced more American military generals than any program outside the service academies. The drill field is used for daily Corps formations, formal reviews, inspections, and the ceremonies that mark the Corps calendar. On football Saturdays, watching the entire Corps march from Simpson to Kyle Field is one of the great spectacles in college sports — 2,000 uniformed cadets in precise formation, passing through crowds of fans, accompanied by the A&M band. The march takes about 20 minutes and draws spectators specifically to watch it.", 240),
            NarrationData("deepdive", "The Corps of Cadets at Texas A&M is one of the most studied military training programs outside the federal academies, because its hybrid civilian-military structure — voluntary participation at a civilian university — has produced military leadership at a rate comparable to service academies. Studies of general officer production through the 20th century consistently show A&M in the top three or four institutions nationally, alongside West Point and Annapolis. The transition from mandatory to voluntary Corps in 1965 was the most controversial decision in A&M's history. Enrollment had stagnated: A&M had about 7,500 students in the early 1960s, while the University of Texas was growing rapidly. Male students who did not want military training simply went elsewhere. Rudder argued that making the Corps voluntary would allow A&M to grow while preserving the Corps as a strong voluntary organization. Critics predicted the Corps would wither. Instead it remained at roughly 2,000 students — self-selected, highly motivated, and arguably more effective than a larger mandatory program. The Corps traditions on the drill field include Fish Week (freshman initiation), formal Corps reviews (dress uniform inspections held several times per year), and the Distinguished Student review at the end of each semester. The march to Kyle Field on football Saturdays follows a specific route and timing choreographed to deliver the Corps to their section of the stadium before kickoff. The Ross Volunteers — the Corps' elite honor guard — march separately and serve at Silver Taps, at the Texas Governor's inauguration, and at state funerals. The Aggie Band, one of the largest military marching bands in the country with over 300 members, accompanies Corps formations and performs the most complex military march shows in college football.", 600),
        ],
    ),
    POIData(
        position=7, name="Bonfire Memorial", tagline="Remembering November 18, 1999",
        lat=30.6153, lng=-96.3355, gps_radius_m=30, walk_note="5 min walk southeast",
        categories=["History", "Student Life"],
        narrations=[
            NarrationData("snapshot", "On November 18, 1999, at 2:42am, the Aggie Bonfire — a 59-foot log stack built by students before the Texas game — collapsed. Twelve students died. The tradition had run since 1909. The memorial, dedicated in 2004, has 12 portals — one for each student — arranged in a spiral. It is one of the most affecting memorials on any campus in America.", 90),
            NarrationData("guide", "The Aggie Bonfire was one of the most distinctive traditions in American college football: since 1909, students had built a massive bonfire the week before the Thanksgiving game against the University of Texas, burning it the night before the game in a ceremony that drew tens of thousands. By the 1990s, the stack had grown to 55 feet — logs cut by student work parties called 'cuts,' stacked in intricate layers over weeks, then lit by torchlight. On November 18, 1999, at 2:42am, during construction, the 59-foot stack collapsed. Twelve students died. Twenty-seven more were injured. The university suspended the tradition. An independent commission investigated the collapse. The official Aggie Bonfire has never returned to campus. The memorial, designed by landscape architects, was dedicated in 2004. Twelve portals — one for each student who died — are arranged in a spiral on a hillside. An eternal flame burns at the center. The inscriptions are spare and specific: each portal carries a name, a class year, a branch of study. Walking through the portals in silence is one of the most emotionally precise experiences on any American campus.", 240),
            NarrationData("deepdive", "The Aggie Bonfire began in 1909 as a small trash fire — students burning debris before the Texas game. Over nine decades it grew into a massive engineering project: students organized themselves into 'cut' crews, went to forests in the surrounding countryside, cut trees, hauled them to campus, and stacked them in a precise wedding-cake configuration under the supervision of experienced upperclassmen. The stacking technique was passed down through generations: center pole logs, outer logs angled inward at specific degrees, log lengths calculated to maintain structural integrity as the stack grew. By the 1990s the stack reached 55 feet and required weeks of labor from thousands of students. The social bonding created by 'cuts' was considered central to the Aggie experience — sleeping in the woods, cutting trees, working alongside seniors who had done it before. The 1999 collapse investigation found that the structural stacking method had accumulated flaws over decades: the wire-and-pin connections between log layers were under increasing stress as the stack grew taller, and the specific 1999 configuration had load-bearing problems that were not visible to the workers. The collapse happened at 2:42am, when 50-70 students were working on the stack. Twelve were killed when logs fell on them. The twelve: Christopher Breen, Michael Ebanks, Jerry Don Self, Bryan McClain, Timothy Kerlee Jr., Chad Powell, Jamie Hand, Nathan Scott West, and four others. Each had a specific story, a specific connection to A&M, a specific reason to be working at 2:42am on a November night. The commission report found systemic safety failures. A&M accepted responsibility. The student-organized off-campus Aggie Bonfire has continued since 2002 — smaller, professionally safety-managed, held off university property. It draws tens of thousands of alumni. The memorial's design was selected through a national competition. The architects chose a spiral of 12 portals because it requires visitors to walk through — not just around — the memorial, making the experience active rather than passive.", 600),
        ],
    ),
    POIData(
        position=8, name="Albritton Bell Tower", tagline="Gateway to Campus · 138-Foot Campus Landmark",
        lat=30.6215, lng=-96.3385, gps_radius_m=35, walk_note="10 min walk north",
        categories=["Architecture", "History"],
        narrations=[
            NarrationData("snapshot", "The Albritton Bell Tower rises 138 feet at A&M's main entrance and has a 49-bell carillon that chimes every 15 minutes. Completed in 1999 for A&M's 125th anniversary, it solved a problem the sprawling campus always had: no single landmark you could point to and say, that's Texas A&M. The inscription at the base: 'From the Brazos to the Seven Seas, Aggies have served their state and nation.'", 90),
            NarrationData("guide", "The Albritton Bell Tower was completed in 1999, donated by Joe B. Albritton, a Texas A&M alumnus who built a media empire that included the Washington Star newspaper and Riggs National Bank. The tower stands 138 feet at the main entrance on University Drive, visible from across College Station. The 49-bell carillon was installed by the Schulmerich Carillons company and chimes every 15 minutes. Special carillon concerts are given on major university events. The tower addressed a real problem: Texas A&M's campus sprawls across 5,200 acres, one of the largest in the United States, and had no single iconic visual landmark. Unlike Princeton's Nassau Hall or Michigan's Burton Tower, A&M's central campus had grown organically without a defining focal point. The bell tower gave the university an instantly recognizable gateway image. The inscription at the base summarizes A&M's self-understanding: service beyond the campus, across the world.", 240),
            NarrationData("deepdive", "Joe B. Albritton graduated from Texas A&M in 1951 and built one of the more unusual American business careers of the late 20th century. He acquired the Washington Star in 1974, just as the newspaper was failing — a dramatic bid to challenge the Washington Post's dominance of the capital's newspaper market. The Star folded in 1981, unable to survive competition with the Post in a two-newspaper market that could only support one. Albritton moved into banking, acquiring Riggs National Bank in Washington, D.C. Riggs later became embroiled in a money-laundering scandal involving Augusto Pinochet's Chilean accounts and Saudi Arabian embassy funds — the bank paid a $25 million fine and was eventually sold to PNC Financial Services. Through these turbulent business ventures, Albritton maintained his connection to Texas A&M and made the bell tower donation as a legacy gift. The 49-bell carillon range is specifically designed to allow performance of the complete carillon repertoire. The Schulmerich company that installed the bells is one of the leading carillon manufacturers in the United States, headquartered in Sellersville, Pennsylvania. A carillon is technically defined as a musical instrument with at least 23 bells; 49 bells allows full chromatic range across four octaves. The tower's design reflects a challenge common to late-20th-century American campus architecture: how do you add a landmark to a campus that already has an established visual vocabulary without it feeling arbitrary? The architects chose a modernist interpretation of the tower form rather than Gothic or Classical Revival, which gives it a distinct identity without clashing with A&M's existing architectural diversity. Texas A&M's 5,200-acre campus is one of the largest in the country, encompassing not just academic buildings but agricultural research stations, veterinary facilities, ROTC training areas, and a research park. The sheer geographic scale means that most students experience only a fraction of the campus during their four years.", 600),
        ],
    ),
]


async def _insert_city_tour_pois(
    session: AsyncSession,
    city_params: dict,
    tour_params: dict,
    pois: list[POIData],
) -> None:
    """Shared helper — insert one city + tour + POIs + narrations."""
    city_result = await session.execute(
        text(
            """INSERT INTO cities (name, slug, university, country, state, lat, lng, description, published)
               VALUES (:name, :slug, :university, :country, :state, :lat, :lng, :description, :published)
               RETURNING id"""
        ),
        city_params,
    )
    city_id = city_result.scalar_one()

    tour_result = await session.execute(
        text(
            """INSERT INTO tours (city_id, name, slug, tagline, duration_minutes, distance_meters,
                                  stop_count, categories, published)
               VALUES (:city_id, :name, :slug, :tagline, :duration_minutes, :distance_meters,
                       :stop_count, :categories, :published)
               RETURNING id"""
        ),
        {"city_id": city_id, **tour_params},
    )
    tour_id = tour_result.scalar_one()

    for poi_data in pois:
        poi_result = await session.execute(
            text(
                """INSERT INTO pois (tour_id, position, name, tagline, lat, lng,
                                     gps_radius_m, walk_note, categories)
                   VALUES (:tour_id, :position, :name, :tagline, :lat, :lng,
                           :gps_radius_m, :walk_note, :categories)
                   RETURNING id"""
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
        for n in poi_data.narrations:
            await session.execute(
                text(
                    """INSERT INTO narrations (poi_id, depth_tier, script, duration_sec)
                       VALUES (:poi_id, :depth_tier, :script, :duration_sec)"""
                ),
                {"poi_id": poi_id, "depth_tier": n.depth_tier, "script": n.script, "duration_sec": n.duration_sec},
            )
    logger.info("Seed: %s committed.", city_params["name"])


async def seed_database() -> None:
    """Seed the database with all city tour data if not already seeded."""
    # Princeton
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT id FROM cities WHERE slug = 'princeton' LIMIT 1")
        )
        if result.scalar_one_or_none() is None:
            logger.info("Seed: Inserting Princeton University tour data...")
            await _insert_city_tour_pois(
                session,
                city_params={
                    "name": "Princeton", "slug": "princeton",
                    "university": "Princeton University",
                    "country": "US", "state": "NJ",
                    "lat": 40.348200, "lng": -74.659300,
                    "description": PRINCETON_DESCRIPTION, "published": True,
                },
                tour_params={
                    "name": "Historic Princeton Campus Walk",
                    "slug": "historic-campus",
                    "tagline": "270 years of history, science, and power — on foot",
                    "duration_minutes": 75, "distance_meters": 2800,
                    "stop_count": 7, "categories": ["History", "Architecture", "Student Life"],
                    "published": True,
                },
                pois=PRINCETON_POIS,
            )
            await session.commit()
        else:
            logger.info("Seed: Princeton already exists — skipping.")

    # UMICH
    async with AsyncSessionLocal() as session:
        r = await session.execute(text("SELECT id FROM cities WHERE slug = 'ann-arbor' LIMIT 1"))
        if r.scalar_one_or_none() is None:
            logger.info("Seed: Inserting University of Michigan tour data...")
            await _insert_city_tour_pois(
                session,
                city_params={
                    "name": "Ann Arbor", "slug": "ann-arbor",
                    "university": "University of Michigan",
                    "country": "US", "state": "MI",
                    "lat": 42.2780, "lng": -83.7382,
                    "description": (
                        "The University of Michigan's Ann Arbor campus is one of the most beautiful "
                        "and academically distinguished research universities in the world. Founded in 1817, "
                        "Michigan's 3,100-acre campus blends Gothic and modern architecture with Big Ten athletics, "
                        "Nobel Prize-winning research, and a vibrant college town culture."
                    ),
                    "published": True,
                },
                tour_params={
                    "name": "University of Michigan Highlights Walk",
                    "slug": "umich-highlights",
                    "tagline": "The Leaders and Best — from The Big House to the Law Quad",
                    "duration_minutes": 70, "distance_meters": 3200,
                    "stop_count": 8, "categories": ["History", "Architecture", "Student Life"],
                    "published": True,
                },
                pois=UMICH_POIS,
            )
            await session.commit()
        else:
            logger.info("Seed: Ann Arbor already exists — skipping.")

    # Texas A&M
    async with AsyncSessionLocal() as session:
        r = await session.execute(text("SELECT id FROM cities WHERE slug = 'college-station' LIMIT 1"))
        if r.scalar_one_or_none() is None:
            logger.info("Seed: Inserting Texas A&M tour data...")
            await _insert_city_tour_pois(
                session,
                city_params={
                    "name": "College Station", "slug": "college-station",
                    "university": "Texas A&M University",
                    "country": "US", "state": "TX",
                    "lat": 30.6185, "lng": -96.3371,
                    "description": (
                        "Texas A&M University is one of the largest universities in the United States, "
                        "with over 74,000 students and a campus defined by military tradition, fierce school "
                        "spirit, and a unique culture unlike any other university in America. Founded in 1876 "
                        "as the state's first public institution of higher education, Aggie culture runs deep."
                    ),
                    "published": True,
                },
                tour_params={
                    "name": "Texas A&M Spirit & Tradition Walk",
                    "slug": "tamu-spirit",
                    "tagline": "Gig 'em — the traditions, the spirit, the stories behind the Aggies",
                    "duration_minutes": 65, "distance_meters": 2800,
                    "stop_count": 8, "categories": ["History", "Student Life", "Architecture"],
                    "published": True,
                },
                pois=TAMU_POIS,
            )
            await session.commit()
        else:
            logger.info("Seed: College Station already exists — skipping.")
