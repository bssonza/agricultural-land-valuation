# Agricultural Land Valuation
Monte Carlo Simulator for Agricultural Land Valuation.

## Introduction
Investing is hard. To do it well, one must not acquire an asset by paying more than it is intrinsically worth. But how to evaluate the worth of a given asset?

An approach is to do a disconted cashflow analysis (DCF) of the respective investment. That is to say, calculate how much cash it will generate in it's lifetime and subtract the opportunity cost of not investing in anything else. 

**This project aims to help users make better investments in the agricultural sector by estimating how much a piece of land is worth by doing this DFC analysis in thousand of possible cenarios of agricultural production.** 

## How does it work

It draws random values for a number of parameters such anual production, costs, commodity prices, real interest rates from a user defined distribution and calculates the yearly cash gerated based on in the values drawn; summing the cashflows of multiple years (a timeline) and subtracting the oportunity costs (real interest rate) gives the Net Present Value (NPV). This is processed is then repeated for thousand of timelines to give a NPV distribution.

## Installation

## Usage
