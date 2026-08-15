#ifndef PI_CONTROLLER_H
#define PI_CONTROLLER_H

typedef struct
{
    float kp;
    float ki;
    float integral;
    float output_min;
    float output_max;
    float integral_min;
    float integral_max;
} PI_Controller_t;

void PI_Init(PI_Controller_t *controller,
             float kp,
             float ki,
             float output_min,
             float output_max,
             float integral_min,
             float integral_max);

void PI_Reset(PI_Controller_t *controller);

float PI_Update(PI_Controller_t *controller,
                float setpoint,
                float measurement,
                float dt);

/*
 * Interface skeleton only; not enabled or validated.
 * Future:
 * - anti-windup strategy selection and verification
 * - derivative not required initially
 * - fixed sample time evaluation
 */

#endif /* PI_CONTROLLER_H */
