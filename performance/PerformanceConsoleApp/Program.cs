﻿﻿using System;
using PerformanceConsoleApp.Services;

class Program
{
    static void Main(string[] args)
    {
        var performanceTest = new PerformanceTest();
        performanceTest.RunPerformanceTest(5000);

        Console.WriteLine("\nPress any key to exit...");
        Console.ReadKey();
    }
}
