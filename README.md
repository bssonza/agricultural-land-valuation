# Agricultural Land Valuation
Monte Carlo Simulator for Agricultural Land Valuation.

## Introduction
Investing is hard. To do it well, one must not acquire an asset by paying more than it is intrinsically worth. But how to evaluate the worth of a given asset?

An approach is to do a disconted cashflow analysis (DCF) of the respective investment. That is to say, calculate how much cash it will generate in it's lifetime and subtract the opportunity cost of not investing in anything else. 

**This project aims to help users make better investments in the agricultural sector by estimating how much a piece of land is worth by doing this DFC analysis in thousand of possible cenarios of agricultural production.** 

## How does it work

It draws random values for a number of parameters, such anual production, costs, commodity prices, real interest rates, from a user defined distribution and calculates the yearly cash gerated based on in the values drawn; summing the cashflows of multiple years (a timeline) and subtracting the oportunity cost (real interest rate) gives the Net Present Value (NPV) of the land. This is processed is then repeated for thousand of timelines to give a NPV distribution.

## Installation
1. Clone and download this repo
2. Extract files to a directory of choice
3. Run AgriculturalLandValuation.py through your prefered IDE

TBI: Download the executable here.

## Usage
This program comes with a User Interface that allows for quick iteration of possible parameters. An example of such iteration:

![AgriculturalLandValuationDemo](https://user-images.githubusercontent.com/61105391/120420949-c2958e00-c33b-11eb-8430-8140f5909b02.gif)

In the example above, the estimated maximum anual production is changed from 70 to 90 bags per years. Acordingly, the average Net Present Value changed from ~R$61,000.00 to ~R$ R$72,000.00.

Each parameter must be provided with a minimum, most likely, and maximum possible value in order to construct and internal triangular distribution.

Any constant parameter (such as tax rate in the example above) can set to that constant in all three fields.

In order to estimate land value in dollars, set dolar price parameter to 1 in all fields.

## License

MIT License

Copyright (c) 2021 bssonza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
