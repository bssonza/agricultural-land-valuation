# Agricultural Land Valuation
Monte Carlo Simulator for Agricultural Land Valuation.

## Introduction
Investing is a challenging endeavor. To excel in it, one needs to purchase an asset at a price lower than its intrinsic value. However, determining the intrinsic worth of an asset poses a significant challange.

One method to assess an asset's value is through Discounted Cash Flow (DCF) analysis. This involves estimating the total cash that the investment will produce over its lifetime and then deducting the opportunity cost associated with forgoing other investments.

This project is designed to assist users in estimating the value of agricultural land through DCF analysis across thousands of potential scenarios.

## How does it work

The methodology hinges on randomly selecting values for key parameters, including annual production, costs, commodity prices, and real interest rates, from a triangular distribution defined by the user. By utilizing these randomly drawn values, the yearly cash generated is calculated. The sum of these cash flows across multiple years, adjusted for the opportunity cost represented by the real interest rate, results in the Net Present Value (NPV) of the land. This calculation process is replicated across thousands of different timelines to produce a distribution of NPV estimates, offering a comprehensive view of the potential financial outcomes for the land investment.

## Installation
1. Clone and download this repo
2. Extract files to a directory of choice
3. Run AgriculturalLandValuation.py

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
