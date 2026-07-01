# data-commons
Emily Reardon 
Collecting and Using the Data Commons
Final Project
Summer 2026

Prompt: 
Datasets from two or more data platforms.
With at least one of them being a data commons (OpenStreetMap, Wikidata, Inaturalist, etc)
You can collect or transform existing data focusing on your topic of your interest.
Then pick a method of data analysis and visualization (graphs, web map)
ArcGIS Online
Google Sheets
Leaflet , Maplibre
Etc
 Write an essay with at least two paragraphs describing:
Insights (if any)
How the data was collected (by you or the source)
How the data was analyzed
Drawbacks/difficulties of using such data.



INTRODUCTION
My background is in Public Education and Public Media, and I’m interested in how we might defend, redesign and rebuild public systems that love us--especially as those systems suffer attack and democracy falters under Big Tech. Grounded in open and ethical tools and processes, my experiments ask how digital technologies might deepen, rather than displace, our relationships with one another as well as the worlds we inhabit to build more just and loving futures.

DATA COLLECTION
I am therefore interested in civic engagement, agency and participation via personal habit. I explored local, quotidian, ‘low stakes/non-presidential’ or ‘off-year’ election data, and on the city data platform, NYC Open Data, I found voter registration and turnout by NYC Community District. I chose data from the 2023 general election; it’s an ‘off-year’ with no citywide races, excluding City Council, so is considered lower stakes than other races. 2023 also is less impacted by social and health concerns surrounding the pandemic and has full Community District coverage. I had hoped to use the recent 2026 elections, but learned that electoral data detail and organization, such as community district indexing, takes time and is not yet available. I exported the data as CSV. 

As an MFA student with deep experience in Public Media and Public Education, I thought it might be interesting to look at civic engagement with respect to ‘art.’ In particular, I was wanted to learn about Public Art and its impact, which I don’t have any expertise in. To explore a second type of open data, I chose a data commons, Open Street Map, which felt interesting as that data is already a type of civic engagement. This data type is only crowd-sourced which introduces a range of strong biases -- for example, who, where, and why an individual might submit data in a location is determined by socio-cultural constructs. Further, what constitutes Public Art is slippery: it’s generally assumed to be freely accessible art forms, but what type of access and which forms constitute ‘art’ are both negotiable. For my interests, I was curious about how public money and systems support Public Art and civic engagement, and only crowd-sourced data does not include that provenance; OSM contributors tag anything they consider public art, from publicly funded installations to graffiti to religious statues, from permanent to temporary, they also tend to drop a pin without filling in name or artist fields. Despite these issues clouding my exploration, I queried tourism=artwork across NYC bounds, and downloaded the data as GeoJSON. 

DATA VISUALIZATION
I chose Leaflet for data visualization because it is widely used in my field and I wanted to deepen my experience with it. I first added the NYC voter data and greyscale color-coded the Community District by voter turnout rates. I added the tourism=artwork data from the OSM data commons, then played with interface design by hand, just as we did in class and as I did in the Leaflet Lab assignment. 


I then got really into the aesthetics to get the digestibility and artistic look & feel I wanted, I used a bit of Claude. Claude work is limited to: 
Color-coding artwork location points in hex colors from one of my favorite public artworks, a subway mosaic mural by the CUNY collective, Hilma’s Ghost (see image below)
Mapping waterways to this hex: 5f78c4, all non-nyc land to this hex: a6c75, and the selected Community District to this hex: b9859c, all of which are from the Hilma’s Ghost artwork. 
Isolating artwork location points so we only see them when zoomed into that Community District. Since the OSM data is biased, with more points in more touristic areas, it was  misleading to see the artwork plotted across the city
Making the key easy to digest and interactable so clicking on a Community District in the key zooms the map view to that district
Masking non-NYC town names


ANALYSIS
Public election turnout is notoriously low, despite wide-ranging efforts to increase participation. Even in ‘high-stakes’ elections 60% turnout is considered robust. In this ‘low stakes’ 2023 race engagement is significantly lower, with only 5-25% of voters participating. 


That engagement with public art might correlate to engagement in public elections can’t be answered by this data, given the inherent biases of the public art data source. However, I learned more about open data and open tech infrastructure as well as a new to me aspect of public systems, Public Art from this exercise and course. 


As a systems designer, I believe in the power of public systems for future justice, and that wide-ranging public systems can support living systems and infrastructures of care, rather than control. I love to think that Public Art has a direct impact on public democracy, and that art might ignite the reimagining and rebuilding we need, as artists have long instigated change by helping to envision alternate futures. I hope to help defend Public Education and Public Media, using Public Art -- and vice versa. 









Source: https://news.artnet.com/art-world/hilmas-ghost-mta-commission-grand-central-2645040

