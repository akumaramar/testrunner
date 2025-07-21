using System.Collections.Generic;

namespace PerformanceConsoleApp.Models
{
    public class DataRowObject
    {
        public Dictionary<string, object> Columns { get; set; } = new Dictionary<string, object>();
        public RowState RowState { get; set; }
    }

    public class DataTableObject
    {
        public List<DataRowObject> Rows { get; set; } = new List<DataRowObject>();
    }

    public class TreeView
    {
        public string Name { get; set; }
        public string EntityName { get; set; }
        public string ParentFieldName { get; set; }
        public string KeyFieldName { get; set; }
    }

    public class TreeDataView
    {
        public string ParentKey { get; set; }
        public List<object> ParentValue { get; set; }
        public DataRowObject Row { get; set; }
    }

    public enum RowState
    {
        Detached = 1,
        Unchanged = 2,
        Added = 4,
        Deleted = 8,
        Modified = 16
    }
}
