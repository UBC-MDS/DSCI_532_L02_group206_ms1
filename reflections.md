# Milestone 2 Reflections
## App Limitations & Possible Improvements:
The 5th plot (boxplot of “Time spent in shelter”) has a log-transformation on the y-axis as the distributions seem to follow a power-curve. This is a limitation of the data, and also partly a limitation of Altair’s plotting manipulation of the y-axis as we cannot adjust it to make it more interpretable than what it already is. Thus, consumers of the visualisation may have to be warned on how to interpret the values on the y-axis. By default, the boxplot of Altair comes with enabled interactive depicting the quantiles breakdown. This also helps the user to extract out quantifiable summaries which mitigates the effect of the possibly confounding log-transformed y-axis.

In the dashboard, the information regarding age distribution of the intake animal can be seen. Drawing a similar parallel to that, a plot depicting age distribution of the out-take animal can be added in the future to help the shelter staff get more information on the age of the animals in the shelter.

Within the application, we create a General Filter for the timeframe, while also embedding specific filters for certain plots. Improvements in CSS or application HTML design would actually help users visualise how the filters relate to the plots.  

## Feedback and Rectification
Our TA gave us generally positive feedback but also highlighted some issues that we can improve on:

__1. We were not utilising Github’s issues functionality as often as we could__  
We utilised other modes of communication that we were very familiar with (such as Slack chat groups). Within these modes of communication, we also made it a point to create meeting summaries/to-do lists that anchored our project progress. With that in mind, we also do admit that we could learn how to use Github’s issues functionality more as it allows for proper documentation of every issue. Unfortunately, we only learned about this in our Lab session on Wednesday, but by then, we had sufficient discussion internally that most of our project tasks completed. 

__2. Our research questions were not clearly stated in our App description__  
We also rectified this by updating our Application description with proper research questions that tie in greatly with the envisioned use cases for our users to improve their operations. 

__3. Team Contract could be more clearly defined in terms of workload breakdown__  
Our initial team contract was based on general collaborative principles, and at the point of its creation, we did not want to create highly specific wording that binds us excessively. Our team was in agreement with the general principles (such as proper division of tasks and accountability or meetings should end with summarised deliverables with assignments and deadlines, etc), instead of highly specific wording that may not allow us to be flexible. To address the feedback, we revised our team contract with more specificity on terminology.

## Learnings 
Our team felt a sense of achievement and are particularly happy about how the app turned out. We were glad to learn and apply the techniques of Dash app applications, and we feel that the overall product was particularly effective for the envisioned use case. 

# Milestone 3 Reflections
## Feedback from users

### What users liked:
Several users liked the logo and found it appealing. Additionally, users also liked the trend chart and found meaningful insights to it. The 5th plot was also a key chart of interactive exploration as the data was particularly novel to them.

### What users thought could be improved:
Some users found it easy to interact with our App but they were not too sure about what research questions the app was trying to answer. Thus, one solution that was suggested was that we should have some form of onboarding information to contextualise what the app was trying to achieve. Specific suggestions included an introductory text on the top, and also for us to put our contact information so that if there were any further questions on the app, they can contact us.

Users also pointed out that it was not too clear that the intended global filter of year range affected all the plots, which we recognise as part of our UI limitations since we did not know enough HTML to create a proper layout. Part of the issue was that the app required a lengthy screen “real-estate” which requires some degree of scrolling, and some users were playing with the time filter and scrolling down to see if there were any changes to the plot. 

In Plot 1 (Overall trends of Intake and Outtake trends), the line chart did not display tooltip information about specific Intake/Outtake points when a cursor was hovered. Several users also pointed out that a tooltip with interaction would be much better in conveying information.

Many users found the 5th plot (boxplot of time spent in shelter before outtake) very interesting to play with. Some users even suggested using that as our main plot instead of Plot 1. 

After becoming attuned with Plots 2 and 3, some users were very interested in comparing the weekday average intake/outtake volumes between different animals (for example comparing Cats and Dogs Intake volume on Mondays in December). 

On a similar vein, some users also wanted to see specific animal Intake/Outtake volume trends in Plot 1, and suggested for a global Animal type filter.

For more details on our overall feedback, please refer to this link:  
https://github.com/UBC-MDS/DSCI_532_L02_group206_ms1/issues/32

## What we changed in this iteration
After a team discussion on the feedback and our overall time constraints, the team decided to focus on certain aspects of revamp for our Python Altair app:
- Under time constraints considerations, instead of providing a chunk of introductory app information which will probably require extensive HTML/layout re-arrangements, we created a title for the app to be placed under the logo. This will hopefully provide some form of contextual onboarding information for the users.
(https://github.com/UBC-MDS/DSCI_532_L02_group206_ms1/issues/34)
- We shifted the Global Year range filter to the top of the app so that it will be the first thing the users encounter. This might give some intuition that the filter is acting globally on all the plots. We also changed the title of the filter to make it more explicit in terms of the data filtering.
(https://github.com/UBC-MDS/DSCI_532_L02_group206_ms1/issues/36)
- We standardised the use of the word “Outakes” to “Outtakes”
(https://github.com/UBC-MDS/DSCI_532_L02_group206_ms1/issues/35)
- The tooltip for Plot 1 was updated to give direct point information of Intake/Outake volumes for that specific month when a cursor was hovering.
(https://github.com/UBC-MDS/DSCI_532_L02_group206_ms1/issues?q=is%3Aissue+is%3Aclosed)
- We changed the Radio buttons Filter for Plot 5 to a Droplist 
(https://github.com/UBC-MDS/DSCI_532_L02_group206_ms1/issues/37)

We also performed some docstrings updates and re-factored certain code such as using list comprehension for the Month filter for Plots 2 and 3. However, some filters (such as the Animals filter for both Plot 2 and 3, and the Intake Health Condition filter for Plot 5) were left untouched as we needed them in a specific display order, and the team felt like it was redundant specifying the options in a list before unpacking them in a list comprehension.
(https://github.com/UBC-MDS/DSCI_532_L02_group206_ms1/issues/39)

## What we chose not to do
Creating a Global Animal filter: 
- The global animal filter might not be compatible with the inclusion of Plot 5 (time spent in shelter for different animals with filter of intake health conditions) because there might not be data for certain animal types (Birds) with specific intake health conditions. Thus to avoid creating an empty Plot 5 due to lack of data for specific combination of filters, we decided not to implement it.
- Putting some onboarding text information at the top: Due to time constraints, we felt that we could not execute this point without spending a lot of time on it. Thus we compromised with a title instead.
- Axis titles abbreviation for Weekdays in Plot 2 and 3: We felt like this was not that critical and chose not to prioritise this.
Legend of Plot 1 embedded inside plot: We chose to keep the legend inside the plot because if it was outside, Plot 1 will not be centered. 

## Wishlist
- Revamp the top of the app with a Jumbotron and contextual information for users to understand the app use cases.
- Put our contact information on the App 

## Experience from being a “fly-on-the-wall”
Everyone felt that this experience of collating feedback from being a “fly-on-the-wall” was extremely useful. Every project requires validation and it was interesting obtaining unbiased feedback via this process. 

Throughout this project, we were playing the roles of app developers with our perspectives of what we think was useful to the users, and sometimes focusing on those unvalidated perspectives created a bias. 

Through this small role-playing of user-group testing, not only did we confirm what we thought were limitations of our apps, but we also uncovered perspectives on app usage that were in our “blindspots”. 

## General Reflections
With the user-feedback, the team prioritised and addressed key issues that led to improvements in the user experience of the app. It was an interesting experience indeed and all of us learnt a lot through this three weeks. We discovered that users are really interested in the data of the app, and it was fun to watch them tinkering with the app. There is a general sense of achievement when users could relate to the use-cases of the app and its intended target audience, which is to help shelter staff answer operational questions about their animal shelter.
