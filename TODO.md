## Greetings
First of all, thanks for this cool assignment and the opportunity to show a little more of my experience.

-- Danilo Paes

---

## The application

I created a makefile to hold the main commands, like starting a docker, running linters and tests to make It simpler to execute.
The regex would search the whole gist string and return It In case of finding that pattern.
We have a couple of exceptions to handle possible errors as well.

Hope you like It :)

---

## Running the application
In order to run you application, you must have `docker` installed in your machine.
1. To start it, just run `make run` inside the root folder, where our `makefile` is settled.

---

## QA
**Q:** Can we use a database? What for? SQL or NoSQL?

**A:** Yes, we definitively could. The approach of using a DB would be related to control of requests.
Of course we could also save our requests to make a history of change (maybe) for each gist but not for querying the response to the user once the gist could be changed and we would be informing old values to our user.
For the purpose of saving for history I would go for a NoSQL approach, once we're already receiving some sort of documents/JSON.

**Q:** How can we protect the api from abusing it?

**A:** Limiting the amount of requests per token - yeah, we should create those as well. We could simply count the amount of requests per day or hour and check If the user already fulfilled his request amount.

**Q:** How can we deploy the application in a cloud environment?

**A:** There's some different ways we can do that. Considering that we're not accessing any internal resource (database for obtain the data for example), and we're acting like a some sort of proxy, we could go for a lighter cloud environment, like Digital Ocean, for example (of course we could use others like GCP or AWS). We could create some KS8 clustering, configurate loading balancing and the amount of PODs depending of the amount of requests expected.

**Q:** How can we be sure the application is alive and works as expected when deployed into a cloud environment?

**A:** We can do a some sort of checkings, like a health checking on Kubernetes, work with replicas and also ensure that the container would be restarted once It fails or crash in some way. And also we could create some alerts, logging structure using tools like Grafana, Sentry, etc.

**Q:** Any other topics you may find interesting and/or important to cover

**A:** I would definitively use caching in this api, storing the responses for a short time. Our cache could be fulfilled with a schedule procedure (for the most researched users) and something like that, to reduce the amount of requests to gists endpoints and increase our performance.