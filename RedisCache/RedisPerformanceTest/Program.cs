﻿using System.Diagnostics;
using StackExchange.Redis;
using System.Text.Json;

class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Category { get; set; } = string.Empty;
    public List<string> Tags { get; set; } = new List<string>();
}

class Program
{
    private static readonly string RedisConnectionString = "localhost,connectTimeout=700,responseTimeout=2000,syncTimeout=1000,connectTimeout=1500";
    private static readonly ConnectionMultiplexer redis = ConnectionMultiplexer.Connect(RedisConnectionString);
    private static readonly IDatabase db = redis.GetDatabase();

    static async Task Main(string[] args)
    {
        try
        {
            Console.WriteLine("=== Redis Performance Test Starting ===\n");

            // Test with small dataset
            await TestSmallDataSet();

            // Test with large dataset
            await TestLargeDataSet();

            Console.WriteLine("\n=== Test Complete! Press any key to exit... ===");
            Console.ReadKey();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
        finally
        {
            redis.Close();
        }
    }

    private static async Task TestSmallDataSet()
    {
        Console.WriteLine("=== Testing with Small Dataset (10 products) ===");
        var products = GenerateProducts(10);
        
        // Store data
        var sw = Stopwatch.StartNew();
        await StoreData("small-dataset", products);
        sw.Stop();
        Console.WriteLine($"Storage Time: {sw.ElapsedMilliseconds}ms");

        // Retrieve data
        sw.Restart();
        var retrievedProducts = await RetrieveData<List<Product>>("small-dataset");
        sw.Stop();
        Console.WriteLine($"Retrieval Time: {sw.ElapsedMilliseconds}ms");
        Console.WriteLine($"Retrieved {retrievedProducts?.Count ?? 0} products\n");
    }

    private static async Task TestLargeDataSet()
    {
        Console.WriteLine("\n=== Testing with Large Dataset (10000 products) ===");
        var products = GenerateProducts(10000);
        
        // Store data
        var sw = Stopwatch.StartNew();
        await StoreData("large-dataset", products);
        sw.Stop();
        Console.WriteLine($"Storage Time: {sw.ElapsedMilliseconds}ms");

        // Retrieve data
        sw.Restart();
        var retrievedProducts = await RetrieveData<List<Product>>("large-dataset");
        sw.Stop();
        Console.WriteLine($"Retrieval Time: {sw.ElapsedMilliseconds}ms");
        Console.WriteLine($"Retrieved {retrievedProducts?.Count ?? 0} products\n");
    }

    private static List<Product> GenerateProducts(int count)
    {
        var products = new List<Product>();
        var categories = new[] { "Electronics", "Clothing", "Books", "Food", "Toys" };
        var random = new Random();

        for (int i = 0; i < count; i++)
        {
            products.Add(new Product
            {
                Id = i + 1,
                Name = $"Product {i + 1}",
                Description = $"This is a detailed description for product {i + 1} with lots of details about its features and specifications.",
                Price = (decimal)Math.Round(random.NextDouble() * 1000, 2),
                Category = categories[random.Next(categories.Length)],
                Tags = Enumerable.Range(0, random.Next(1, 6))
                    .Select(_ => $"Tag{random.Next(1, 21)}")
                    .ToList()
            });
        }

        return products;
    }

    private static async Task StoreData<T>(string key, T data)
    {
        var jsonData = JsonSerializer.Serialize(data);
        await db.StringSetAsync(key, jsonData);
    }

    private static async Task<T?> RetrieveData<T>(string key)
    {
        var value = await db.StringGetAsync(key);
        if (!value.HasValue)
            return default;

        return JsonSerializer.Deserialize<T>(value!);
    }
}
