/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
static uint32_t adc_raw = 0;
static uint16_t target_raw = 2048;

static int32_t error = 0;

static float kp = 0.010f;
static float ki = 0.002f;

static float integral = 0.0f;
static float control_output = 50.0f;

static uint8_t duty = 50;

static char uart_buf[128];

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */


/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_ADC1_Init();
  MX_USART1_UART_Init();
  MX_TIM3_Init();
  /* USER CODE BEGIN 2 */
  if (HAL_ADCEx_Calibration_Start(&hadc1) != HAL_OK)
  {
      Error_Handler();
  }

  if (HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1) != HAL_OK)
  {
      Error_Handler();
  }

  __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, 500);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  uint32_t test_start_ms = HAL_GetTick();

  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	  uint32_t elapsed_ms = HAL_GetTick() - test_start_ms;

	      if (elapsed_ms < 10000U)
	      {
	          target_raw = 2048;
	      }
	      else if (elapsed_ms < 90000U)
	      {
	          target_raw = 2400;
	      }
	      else
	      {
	          target_raw = 2048;
	      }

	  uint32_t adc_sum = 0U;
	  uint32_t adc_count = 0U;

	  for (uint32_t sample = 0U; sample < 8U; sample++)
	  {
	      if (HAL_ADC_Start(&hadc1) == HAL_OK)
	      {
	          if (HAL_ADC_PollForConversion(&hadc1, 100U) == HAL_OK)
	          {
	              adc_sum += HAL_ADC_GetValue(&hadc1);
	              adc_count++;
	          }
	      }

	      (void)HAL_ADC_Stop(&hadc1);
	  }

	  if (adc_count > 0U)
	  {
	      adc_raw = adc_sum / adc_count;

	      error = (int32_t)target_raw - (int32_t)adc_raw;

	      integral += (float)error * 0.1f;

	      if (integral > 5000.0f)
	      {
	          integral = 5000.0f;
	      }
	      else if (integral < -5000.0f)
	      {
	          integral = -5000.0f;
	      }

	      control_output =
	          50.0f
	          + kp * (float)error
	          + ki * integral;

	      if (control_output > 100.0f)
	      {
	          control_output = 100.0f;
	      }
	      else if (control_output < 0.0f)
	      {
	          control_output = 0.0f;
	      }

	      uint32_t output_x100 =
	          (uint32_t)(control_output * 100.0f + 0.5f);

	      uint32_t arr = __HAL_TIM_GET_AUTORELOAD(&htim3);

	      uint32_t compare =
	          (uint32_t)(((arr + 1U) * control_output) / 100.0f + 0.5f);

	      if (compare > arr)
	      {
	          compare = arr;
	      }

	      __HAL_TIM_SET_COMPARE(
	          &htim3,
	          TIM_CHANNEL_1,
	          compare
	      );

	      duty = (uint8_t)(control_output + 0.5f);

	      int32_t integral_log = (int32_t)integral;
	      uint32_t tick_ms = HAL_GetTick();

	      int len = snprintf(
	          uart_buf,
	          sizeof(uart_buf),
			  "TICK=%lu,ADC=%lu,TARGET=%u,INT=%ld,ERR=%ld,KP=0.010,KI=0.002,OUT=%lu,DUTY=%u\r\n",
	          (unsigned long)tick_ms,
	          (unsigned long)adc_raw,
	          target_raw,
	          (long)integral_log,
	          (long)error,
	          (unsigned long)output_x100,
	          duty
	      );

	      if (len > 0)
	      {
	          HAL_UART_Transmit(
	              &huart1,
	              (uint8_t *)uart_buf,
	              (uint16_t)len,
	              100
	          );
	      }
	  }

	  HAL_Delay(100U);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV2;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
