## Overview
The marketing tracker is a Django application built for me to keep track of my Facebook marketing efforts. It will be run locally on my windows laptop.

The marketing strategy is as follows:
- I've joined 10 business related Facebook groups
- I've split the groups into 2 sets, A and B
- I'll create ads, which may be a combination of text and images, and post them alternating in these group sets:
	- on Monday, Wednesday and Friday I'll post the ad to group A
	- on Tuesday, Thursday and Saturday, I'll post the ad to group B
- the application will list the appropriate set of groups to the application home page on the prescribed day
- I'll enter and keep track of engagements that result from posts to these groups. Engagements will entail:
	- Who made the engagement
	- what was the comment/question
	- any notes on the engagement
- over time, I'd like to be able to determine which ads in which groups posted at which days and time gets the best engagements
## Models
#### FB Group
- Name
- Group url
- Set
#### Ads
- name
- text
- image
#### Post
- ad
- fb group
- post url
- posted at
#### Contact
- name
- fb url
#### Engagement
- contact
- post
- content
- notes
- message url
## Views
#### Home
- Today's date
- List of fb groups in today's set
	- actions: add post
- Post history ordered by last updated descending
	- columns: Date posted, last updated, number of engagements
	- actions: view engagements
#### Ads
- Create new Ad
- List ads by date created descending
#### Contacts
- Create new contact
- List contacts by last engagement
## Frontend UI
The front end design is based on a bootstrap 5 template in the base project directory in a "templates" folder. Within that folder contains another folder called "extras" with additional pages from the original template, but these are just for reference. In the template folder I've already created the base, nav and sidebar components for the layout. Other pages for data entry and display data will follow this layout.
#### Inline Text Formatting
Facebook groups now allows formatting such as bold and italics within their post editor. I would like to implement the same formatting and store textField data  that is compatible with this formatting. At the very minimum, the text editor in my application should give me the ability to select text within the textarea and apply the following:
- Bold
- Italics
- Cursive
- Double Struck
- insert line break

Once text content has been created and formatted the way I want, I'd like to be able to copy it and paste it directly into the facebook post

