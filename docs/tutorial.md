# Tutorial

LC601-5 constant moment beam load cell. Excitation and signal wire pair colors match {numref}`diagram`.

```{figure} _static/tutorial/diagram.png
:name: diagram
:alt: C-Therm manual next to wooden box containing reference samples and glove
C-Therm manual and reference samples
```

The load cell calibration sheet, dated 2019-01-21, excited at 10.000&nbsp;Vdc. The balance is -0.012&nbsp;mVdc, sesnitivity 20.023&nbsp;mVdc, in and out resist are 404.00&nbsp;Ω and 351.70&nbsp;Ω. The 59k shunt is 14.77104.00&nbsp;mVdc. Calibration factors are 2.002&nbsp;mV/V, 59K shunt, 1.477&nbsp;mV/V.

With a sensitivity of ~2&nbsp;mV/V, if the excitation voltage is 10&nbsp;V, the full-scale load of 5&nbsp;lb would correspond to a reading of 20&nbsp;mV on the white/green signal wires. See [general equations](https://support.labjack.com/docs/strain-gauges-app-note#StrainGauges(AppNote)-GeneralEquations) for details.

The DAQ needs sufficient sensitivity to read the smallest increment you're interested in. In the [wiring for raw bridge measurements](https://support.labjack.com/docs/bridge-circuits-app-note#BridgeCircuits(AppNote)-WiringforRawBridgeMeasurements) guide, the built-in excitation voltage for an x201 gain setting and 1.25&nbsp;V offset and the [excitation voltage supply selection](https://support.labjack.com/docs/bridge-circuits-app-note#BridgeCircuits(AppNote)-ExcitationVoltageSupplySelection) suggests we have a 2.5&nbsp;V excitation in this configuration.

At 5&nbsp;lb load, then we should expect a signal of 5.0&nbsp;mV. Let's assume we want to distinguish between 0.1&nbsp;lb difference, this means the DAQ needs to measure 100&nbsp;μV. Our gain of 201 provided by the instrumentation amplifier means that the 100&nbsp;μV signal we're interested in is amplified to 20.1&nbsp;mV.

From the [T7 datasheet](https://support.labjack.com/docs/14-0-analog-inputs-t-series-datasheet#id-14.0AnalogInputs[T-SeriesDatasheet]-T7), on the +-10V channel, with 16-bit resolution, we get about `1e6*20/(2^16-1)` or 300&nbsp;μV resolution. Since we want to discriminate between 20.1&nbsp;mV increments, then we have about ~70 digital "steps" corresponding to 0.1&nbsp;lb difference.

A sensitivity of 2.002&nbsp;mV/V, multiplied through a gain of 201 is 402.4&nbsp;mV/V, meaning a 5&nbsp;lb weight with a 2.5&nbsp;V excitation would cause a 1.005&nbsp;V shift in the reading. In other words, the sensitivity is 4.975&nbsp;lb/V or 2257&nbsp;g/V or 443&nbsp;μV/g.

The reading is offset to 1.25&nbsp;V, so at maximum load, the value should swing from 0.25&nbsp;V to 2.25&nbsp;V.

## To-do

- [ ] Consider the U6-Pro which has a 24-bit ADC to the T7's 16-bit. There's a software compromise here, but the resolution is better.
- [ ] Run these same calculations for a 0.4&nbsp;V offset, 201 gain, on the +-1&nbsp;V range for U6-Pro and T7
- [ ] Also check the flexible IO channelo on the T7, which may provide higher effective resolution
