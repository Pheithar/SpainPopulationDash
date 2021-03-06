# Population growth in Spain

App made with [Dash](https://dash.plotly.com/) to learn how to do interactive plots to display information. The plot I decided to make was the map of population of Spain divided by communities. The data is obtained from the [INE](https://www.ine.es/index.htm), from ['Estadística del Padrón continuo']("https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177012&menu=ultiDatos&idp=1254734710990#).


![Plots](./images/plots.png)


## How to use the map

On top of the map there are some options: `Gender Selector`, `Age Selector`, `Nationality Selector`, `Display in relative values` and `Year Selector`.

Each one allows to update the map with the proper selections. For example, if we want to see the population of foreigner boys between 0 and 4 years in Spain in the year 2012, and we want to see the colors in proportion of the community population, then we would select:

![Selector image](./images/selector.png)

In the map, the communities can be selected to display a detailed information per community in the bottom right plot. To stop seeing the information from that community, you can click again in it.



## Additional information

The code is available at [this repository](https://github.com/Pheithar/SpainPopulationDash) and the deployed app is in [this webpage](https://spain-population-dash.herokuapp.com/). All the code was made by Alejandro ['Pheithar'](https://github.com/Pheithar) Valverde Mahou, following multiple tutorials from [Dash](https://dash.plotly.com/) and [Heroku](https://www.heroku.com). Special thanks to the YouTube chanel [Charming Data](https://www.youtube.com/channel/UCqBFsuAz41sqWcFjZkqmJqQ) for his [tutorial on how to deploy to Heroku](https://www.youtube.com/watch?v=b-M2KQ6_bM4).
