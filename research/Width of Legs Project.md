
Potential Pros and Cons, on current knowledge.

**CoP and IMU**

Potential Pros and Cons

| Pros                             | Cons                                      |
| -------------------------------- | ----------------------------------------- |
| - Simple Calculations            | - Cummulative Error Rate (IMU)            |
| - More accuracy when stationary* | - Abstract Space                          |
| - Easier to model                | - Real time recalculations Recalibration* |
| - Maturity of technology (IMU)   | - One subject per measurement             |

*The Accuracy of the application will depend on the subject when stationary. Also a slight Recalibration will need to be incorporated as readings of the IMU can produce cummulative error, which needs to be mitigated in real time.

The main drawback that such a system may produce is the fact that space is an abstract.

The development of a model that relies on Center of Pressure and the IMU readings of each foot will be dependent on the current tech that we have and the pieces that can be combined to create a model.

As of today, the Center of Pressure algorithm for our custom insoles can be reused for the development of the model. Furthermore the insoles already contain the IMU that can produce accelerometer and gyroscope readings. We can rely on both to triangulate the position of each foot relative to the body. Additional calculation steps that need to be considered are:

- Triangulation calculation for estimating the position of each foot relative to the Center of Pressure
- Calculation of Acceleration and Roration readings at all times to estimate the distance between each foot before and after a motion action
- 

---

 **UWB** 
| Pros                                | Cons                                         |
| ----------------------------------- | -------------------------------------------- |
| - Lower Margin of error             | - Requires Complex Modeling                  |
| - Field of Space                    | - Complexity of Calculations                 |
| - Airtags / Airpods                 | - Signal bypass whgen subject is stationary* |
| - Track multiple subjects at a time |                                              |

*When a subject is stationary the UWB signal will bypass the subject without him being detected, as it relies on dopler effect.



## Algorithm Development




