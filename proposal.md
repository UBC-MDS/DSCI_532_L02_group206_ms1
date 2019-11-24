# Proposal

### Motivation and purpose

Animal shelters serve to provide placement services, medical attention, and shelter to abandoned or injured animals. These shelters act as non-profit organizations, and as a result, they are often strapped for resources and rely heavily on volunteers. These issues are further compounded in animal shelters that implement no-kill policies, such as the [Austin Animal Center(AAC)](http://www.austintexas.gov/department/aac). In particular, two key factors remain paramount, namely, the intake and outtake volumes of animals. Both require extensive resources in terms of either onboarding and discharge procedures. Thus, resource planning and manpower scheduling are important facets of operation management to ensure the sustainability of the shelter.

Our app will serve the shelter staff with visualizations that provide critical information to enable improved staff/volunteer scheduling and resource planning. They can visually gauge the seasonality of intake/outtake volume across time. Users can explore the intake/outtake volumes by animal types across weekdays, and also evaluate if certain factors extend the time spent by animals in the shelter before outtake. They can also easily understand the age distribution of animals upon intake.

By adopting our proposed app, users can obtain insightful perspectives on the shelter’s operations, and make informed decisions about resource planning and staff/volunteer scheduling.

### Description of the data

Our app visualizes a dataset of approximately 70,000 animal intakes at the ACC, in Texas. This is the largest no-kill animal shelter in the United States, providing shelter to over 18,000 animals each year. As part of the AAC's efforts to bring awareness and care for animals in need, the organization makes its accumulated intake and outcomes data available as part of the city of [Austin's Open Data Initiative](https://data.austintexas.gov/browse?q=austin%20animal%20center&sortBy=relevance&utf8=%E2%9C%93).

The dataset contains information on intakes and outcomes of animals entering the AAC from October 2013 to March 2018. Each animal record has 14 associated variables which describe information about the animal itself (animal_type, breed, sex, age), the time frame of the animal's stay in the shelter (intake_monthyear, intake_weekday, total_time_in_shelter_days), and the conditions surrounding the intake and outcome of the animal (intake_condition, intake_type, outcome_type).

### Research questions you are exploring

Peter is a volunteer at the Austin Animal Center with a desire to improve the operations within the shelter. He is overseeing both the scheduling of volunteers and resource budget planning; thus, he seeks to understand the daily demands of the animal shelter. In particular, Peter is especially interested in understanding the daily intake of rescue/abandon animals, as well as, the number of outtake discharges.

By logging on to the app, Peter can glance at the overall intake and outtake trends. Observing that it is now approaching June, where there appears to be a seasonal increase in animal intake numbers, he decides to recruit more volunteers for the summer season.
Below the top graph, Peter is presented with an overview of the average intake and outtake counts on a weekday basis. By filtering across animals, he notices that he should request for more volunteers with cat-handling experience from Mondays to Thursdays. Additionally, based on the age distributions of intake animals, Peter realizes that the ages of the intake cats are likely to be highly concentrated at young ages. This aids his planning of volunteers as he considers enlisting volunteers who are experienced with kittens.

Peter is also presented with an overall view of the time spent in shelter before outtake for each animal type. He postulates that animals that were injured at point of intake tend to spend a longer time in the shelter compared to healthy animals, and can verify that with some selection filtering. He easily understands which animal is the least likely to get adopted and can either improve marketing adoption outreach for that animal type or plan his resource budget to accommodate the operational demands.
