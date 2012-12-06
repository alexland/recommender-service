


![schematic](https://raw.github.com/alexland/recommender-service/master/assets/schematic-1.png)

## Why Implement a Recommendation Engine as a Web Service?

* [separation of concerns](#separation-of-concerns)

* [interface familiar to devs](#familiar-to-devs)

* [ML models can be built & retrained outside of the main app's release cycle](#)

* [the algorithm underlying the RE can be revised or replaced without change to the interface](#)

* [RESTFUL routing is a nice way to implement "context"-dependence without requiring supplied parameters](#)


***

to get a recommendation, just *_curl_* against an endpoint:

    curl http://my-recommender.com/routebeer/route66?user_id=43563



