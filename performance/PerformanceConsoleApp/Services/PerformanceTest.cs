using System;
using System.Collections.Generic;
using System.Diagnostics;
using PerformanceConsoleApp.Models;

namespace PerformanceConsoleApp.Services
{
    public class PerformanceTest
    {
        private static Random random = new Random();

        public void RunPerformanceTest(int recordCount)
        {
            Console.WriteLine("TreeView Performance Test");
            Console.WriteLine("------------------------");

            // Create sample data
            DataTableObject dataTable = GenerateSampleData(recordCount);
            TreeView treeView = new TreeView
            {
                Name = "SampleTree",
                EntityName = "SampleEntity",
                ParentFieldName = "ParentId",
                KeyFieldName = "Id"
            };

            // Test original implementation
            Console.WriteLine("\nOriginal Implementation:");
            var originalBuilder = new TreeViewBuilder();
            var originalResult = TestImplementation(originalBuilder, dataTable, treeView);

            // Create fresh data for second test
            dataTable = GenerateSampleData(recordCount);

            // Test optimized implementation
            Console.WriteLine("\nOptimized Implementation:");
            var optimizedBuilder = new TreeViewBuilderOptimized();
            var optimizedResult = TestImplementation(optimizedBuilder, dataTable, treeView);

            // Compare results
            Console.WriteLine("\nComparison:");
            Console.WriteLine($"Original Time:    {originalResult.time:N2} ms");
            Console.WriteLine($"Optimized Time:   {optimizedResult.time:N2} ms");
            Console.WriteLine($"Original Nodes:   {originalResult.nodes}");
            Console.WriteLine($"Optimized Nodes:  {optimizedResult.nodes}");
            Console.WriteLine($"Improvement:      {((originalResult.time - optimizedResult.time) / originalResult.time * 100):F2}%");
        }

        private (double time, int nodes) TestImplementation(dynamic builder, DataTableObject dataTable, TreeView treeView)
        {
            // Warm-up run
            builder.BuildTreeView(dataTable, treeView);

            // Performance test
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();

            var result = builder.BuildTreeView(dataTable, treeView);

            stopwatch.Stop();

            // Display results
            DisplayResults(dataTable.Rows.Count, result.Count, stopwatch.ElapsedMilliseconds);

            return (stopwatch.ElapsedMilliseconds, result.Count);
        }

        private void DisplayResults(int totalRecords, int nodesCreated, long elapsedMilliseconds)
        {
            Console.WriteLine($"\nPerformance Results:");
            Console.WriteLine($"Total Records: {totalRecords}");
            Console.WriteLine($"Tree Nodes Created: {nodesCreated}");
            Console.WriteLine($"Execution Time: {elapsedMilliseconds:N2} ms");
            Console.WriteLine($"Average Time per Record: {(double)elapsedMilliseconds / totalRecords:F3} ms");
            
            // Memory usage
            long memoryUsed = GC.GetTotalMemory(true);
            Console.WriteLine($"Memory Used: {memoryUsed / 1024:N0} KB");
        }

        private DataTableObject GenerateSampleData(int count)
        {
            var dataTable = new DataTableObject();
            
            // Add root nodes (multiple roots to create wider trees)
            for (int i = 1; i <= 5; i++)
            {
                var rootRow = new DataRowObject { RowState = RowState.Unchanged };
                rootRow.Columns.Add("Id", $"ROOT{i}");
                rootRow.Columns.Add("ParentId", "");
                rootRow.Columns.Add("AlternateId", $"ALT{i}");
                rootRow.Columns.Add("Name", $"Root {i}");
                rootRow.Columns.Add("IsProcessed", false);
                dataTable.Rows.Add(rootRow);
            }

            // Generate hierarchical data with complex relationships
            for (int i = 1; i <= count - 5; i++)
            {
                var row = new DataRowObject { RowState = GetRandomRowState() };
                string id = $"ID{i}";
                string altId = $"ALT{i}";

                string parentId = GetParentId(i);

                row.Columns.Add("Id", id);
                row.Columns.Add("ParentId", parentId);
                row.Columns.Add("AlternateId", altId);
                row.Columns.Add("Name", $"Node {i}");
                row.Columns.Add("IsProcessed", false);
                row.Columns.Add("Depth", GetNodeDepth(parentId));
                row.Columns.Add("HasChildren", random.Next(0, 2) == 1);
                
                dataTable.Rows.Add(row);
            }

            AddSpecialTestCases(dataTable);

            return dataTable;
        }

        private string GetParentId(int i)
        {
            // Create different types of hierarchies
            if (i <= 100) // First 100 nodes directly under root nodes
            {
                return $"ROOT{random.Next(1, 6)}";
            }
            else if (i % 50 == 0) // Every 50th node is a new sub-root
            {
                return $"ROOT{random.Next(1, 6)}";
            }
            else if (i % 7 == 0) // Every 7th node creates a deep path
            {
                return $"ID{Math.Max(1, i - 7)}";
            }
            else // Other nodes randomly assigned
            {
                int parentIndex = Math.Max(1, i - random.Next(1, 20));
                return $"ID{parentIndex}";
            }
        }

        private RowState GetRandomRowState()
        {
            int rand = random.Next(0, 100);
            if (rand < 75) return RowState.Unchanged;  // 75% unchanged
            if (rand < 85) return RowState.Modified;   // 10% modified
            if (rand < 95) return RowState.Added;      // 10% added
            return RowState.Deleted;                   // 5% deleted
        }

        private int GetNodeDepth(string parentId)
        {
            if (parentId.StartsWith("ROOT")) return 1;
            if (parentId.StartsWith("ID"))
            {
                string numStr = parentId.Substring(2);
                if (int.TryParse(numStr, out int num))
                {
                    return (num % 7 == 0) ? num % 5 + 2 : 2; // Creates varying depths
                }
            }
            return 1;
        }

        private void AddSpecialTestCases(DataTableObject dataTable)
        {
            var specialCases = new[]
            {
                (id: "SPECIAL1", parentId: "ID1", altId: "ALTX1", state: RowState.Modified),
                (id: "SPECIAL2", parentId: "SPECIAL1", altId: "ALTX2", state: RowState.Added),
                (id: "SPECIAL3", parentId: "SPECIAL3", altId: "ALTX3", state: RowState.Unchanged),
                (id: "SPECIAL4", parentId: "NONEXISTENT", altId: "ALTX4", state: RowState.Unchanged),
                (id: "SPECIAL5", parentId: "", altId: "", state: RowState.Modified),
            };

            foreach (var specialCase in specialCases)
            {
                var row = new DataRowObject { RowState = specialCase.state };
                row.Columns.Add("Id", specialCase.id);
                row.Columns.Add("ParentId", specialCase.parentId);
                row.Columns.Add("AlternateId", specialCase.altId);
                row.Columns.Add("Name", $"Special Case {specialCase.id}");
                row.Columns.Add("IsProcessed", false);
                row.Columns.Add("Depth", 99);
                row.Columns.Add("HasChildren", true);
                dataTable.Rows.Add(row);
            }
        }
    }
}
