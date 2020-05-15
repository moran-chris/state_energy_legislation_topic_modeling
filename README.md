# State Legislation Topic Modeling 


## Business Case 
Changes in laws and regulations can pose major business risks across all industry sectors. To navigate this risk, companies need to be aware of proposed legislation that could impact their business. Reading over every bill is an inefficient, time consuming and expensive task. 

Machine Learning can vastly reduce this burden through topic modeling. Topic modeling enables companies to filter out bills unrelated to their business and to focus their attention on bills that will most likely affect their operations. 

The below analysis performs topic modeling on state legislation pertaining to the energy sector. However the same framework can be applied to model topics for any of the tracked categories of legislation on the [NCLS' website](https://www.ncsl.org/research/telecommunications-and-information-technology/ncsl-50-state-searchable-bill-tracking-databases.aspx). 

## The Data 

As mentioned above the data used was exctracted from the [NCLS' website](https://www.ncsl.org/research/telecommunications-and-information-technology/ncsl-50-state-searchable-bill-tracking-databases.aspx). The first step in the data collection process was to extract the below table via the database search. 
[]table image
As you can see the bills already have topics assigned to them but many bills are missing values for that field and as shown later much of the value is derrived through modeling subtopics. 

Once the table was extracted Python's BeautifulSoup module was employed to scrape the page's html file in order to navigate to each individual bill link and extract the bill text from each link. 

At this point the dataset contained the following fields: 

-   bill_id (str)
-   title   (str)
-   year    (int)
-   status  (str)
-   topics  (str)
-   summary (str)
-   associated bills (str)
-   date of last action (str)
-   author  (str)
-   text    (str)

Many of these fields contained additional information related to the bill such as authors also containig additional authors. Below are additional features that were extracted from the previous features:
-   state   (str)
-   additional authors (str)
-   primary_dem (int)
-   primary_rep (int)
-   additional_dem (int)
-   additional_rep  (int)

Duplicate bills were identified and removed by locating bills with identical text and state features as well as locating bills with identical bill_ids and author. 

[]image showing html 

Discustion on number of records and how duplicates were removed 

## Topic Modeling Pipeline 

Each document in the coprus for topic modeling was composed of the text feature for each row in the dataset. The first step in preparing the feature for topic modeling was to convert the entire string to lowercase and remove punctuation. Each word was then passed through nltk's wordnet lemmetizer. To reduce the impact of legalize and other non descriptive words a custom stop words list was created and all words in the list were removed. The custom stop words list can be viewed in the file get_stop_words.py located in the src directory. All remaining words in the corpus were then tokenized and a tf_idf matrix was then created using the tokens. Finally, the tf_idf matrix was then passed through a clustering algorithm (KMeans, NMF) to derrive the topics. 

[]image of topic modeling pipeline 

