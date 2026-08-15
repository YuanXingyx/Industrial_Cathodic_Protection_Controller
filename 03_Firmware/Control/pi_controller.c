#include "pi_controller.h"

void PI_Init(PI_Controller_t *controller,
             float kp,
             float ki,
             float output_min,
             float output_max,
             float integral_min,
             float integral_max)
{
    if (controller == 0) {
        return;
    }

    controller->kp = kp;
    controller->ki = ki;
    controller->integral = 0.0f;
    controller->output_min = output_min;
    controller->output_max = output_max;
    controller->integral_min = integral_min;
    controller->integral_max = integral_max;
}

void PI_Reset(PI_Controller_t *controller)
{
    if (controller != 0) {
        controller->integral = 0.0f;
    }
}

float PI_Update(PI_Controller_t *controller,
                float setpoint,
                float measurement,
                float dt)
{
    (void)controller;
    (void)setpoint;
    (void)measurement;
    (void)dt;

    /* Deliberately not implemented until the control-loop prerequisites pass. */
    return 0.0f;
}
