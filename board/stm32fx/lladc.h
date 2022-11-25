// ACCEL1 = ADC10
// ACCEL2 = ADC11
// VOLT_S = ADC12
// CURR_S = ADC13

#define ADCCHAN_ACCEL0 10
#define ADCCHAN_ACCEL1 11
#define ADCCHAN_VOLTAGE 12
#define ADCCHAN_CURRENT 13

void register_set(volatile uint32_t *addr, uint32_t val, uint32_t mask);

void adc_init(void) {
  // ADC_CCR_ADCPRE
  /*
  17:16 ADCPRE: ADC prescaler
Set and cleared by software to select the frequency of the clock to the ADC. The clock is
common for all the ADCs.
Note: 00: PCLK2 divided by 2
01: PCLK2 divided by 4
10: PCLK2 divided by 6
11: PCLK2 divided by 8

define  ADC_CCR_ADCPRE                      0x00030000U        <ADCPRE[1:0] bits (ADC prescaler) 
define  ADC_CCR_ADCPRE_0                    0x00010000U        !<Bit 0 
define  ADC_CCR_ADCPRE_1

*/

  // Set ADC clock prescaler to divide by 4 maybe
  // register_set(&(ADC->CCR), ADC_CCR_TSVREFE | ADC_CCR_VBATE | ADC_CCR_ADCPRE_1, 0xC30000U);
  
  register_set(&(ADC->CCR), ADC_CCR_TSVREFE | ADC_CCR_VBATE, 0xC30000U);
  register_set(&(ADC1->CR2), ADC_CR2_ADON, 0xFF7F0F03U);
  // This should be maxing out the sample interval - 480 cycles
  register_set(&(ADC1->SMPR1), ADC_SMPR1_SMP12_0 | ADC_SMPR1_SMP12_1 | ADC_SMPR1_SMP12_2 |
                               ADC_SMPR1_SMP13_0 | ADC_SMPR1_SMP13_1 | ADC_SMPR1_SMP13_2, 0x7FFFFFFU);
  /*
000: 3 cycles
001: 15 cycles
010: 28 cycles
011: 56 cycles
100: 84 cycles
101: 112 cycles
110: 144 cycles
111: 480 cycles*/
}

uint32_t adc_get(unsigned int channel) {
  // Select channel
  register_set(&(ADC1->JSQR), (channel << 15U), 0x3FFFFFU);

  // Start conversion
  ADC1->SR &= ~(ADC_SR_JEOC);
  ADC1->CR2 |= ADC_CR2_JSWSTART;
  while (!(ADC1->SR & ADC_SR_JEOC));

  return ADC1->JDR1;
}

uint32_t adc_get_voltage(void) {
  // REVC has a 10, 1 (1/11) voltage divider
  // Here is the calculation for the scale (s)
  // ADCV = VIN_S * (1/11) * (4095/3.3)
  // RETVAL = ADCV * s = VIN_S*1000
  // s = 1000/((4095/3.3)*(1/11)) = 8.8623046875

  // Avoid needing floating point math, so output in mV
  return (adc_get(ADCCHAN_VOLTAGE) * 8862U) / 1000U;
}
