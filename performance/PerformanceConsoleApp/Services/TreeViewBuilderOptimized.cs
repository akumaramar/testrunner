using System;
using System.Collections.Generic;
using PerformanceConsoleApp.Models;

namespace PerformanceConsoleApp.Services
{
    public class TreeViewBuilderOptimized
    {
        public List<TreeDataView> BuildTreeView(DataTableObject dataTableObject, TreeView treeView)
        {
            List<TreeDataView> treeDataViews = new List<TreeDataView>();
            if (dataTableObject.Rows.Count < 1 || dataTableObject.Rows[0].Columns.Count < 1)
                return treeDataViews;
            string parentfieldName = treeView.ParentFieldName;
            string[] keyFieldNameList = treeView.KeyFieldName.Split(',');
            string keyFieldName = "";
            string alternatekeyFieldName = "";
            if (keyFieldNameList.Length > 1)
            {
                keyFieldName = keyFieldNameList[0].Trim();
                alternatekeyFieldName = keyFieldNameList[1].Trim();
            }
            else
            {
                keyFieldName = treeView.KeyFieldName;
            }

            List<DataRowObject> currentTableRows = dataTableObject.Rows.FindAll(
                x => x.Columns.Count > 0
                && !x.Columns["IsProcessed"].Equals(true)
                && x.RowState != RowState.Deleted
                );

            foreach (DataRowObject currentRow in currentTableRows)
            {
                if (currentRow.RowState == RowState.Deleted || currentRow.Columns["IsProcessed"].Equals(true))
                    continue;
                DataRowObject parentDataRowObject = currentTableRows.Find(x =>
                                            String.IsNullOrEmpty(alternatekeyFieldName) ?
                                                x.Columns[keyFieldName].Equals(currentRow.Columns[parentfieldName]) :
                                                (x.Columns[keyFieldName].ToString() + x.Columns[alternatekeyFieldName].ToString())
                                            .Equals(currentRow.Columns[parentfieldName]));

                if (
                    parentDataRowObject == null
                    || (parentDataRowObject.Columns[parentfieldName].Equals(String.Empty) && parentDataRowObject.Columns[keyFieldName].Equals(String.Empty))
                    || parentDataRowObject.Columns[keyFieldName].Equals(parentDataRowObject.Columns[parentfieldName])
                    )
                {
                    var keyValue = currentRow.Columns[keyFieldName];
                    List<object> parentKeyList = new List<object>();
                    parentKeyList.Add(keyValue);

                    treeDataViews.Add(new TreeDataView()
                    {
                        ParentKey = "primarykey",
                        ParentValue = parentKeyList,
                        Row = currentRow,
                    });

                    currentRow.Columns["primarykey"] = parentKeyList;
                    currentRow.Columns["IsProcessed"] = true;
                    var groupedRows = dataTableObject.Rows.FindAll(row => !row.Columns["IsProcessed"].Equals(true))
                        .GroupBy(row => row.Columns[parentfieldName].ToString())
                        .ToDictionary(row => row.Key, row => row.ToList());

                    treeDataViews = BuildChildTreeView(currentRow,
                        groupedRows
                        , parentfieldName, keyFieldName, alternatekeyFieldName, treeDataViews, parentKeyList);
                }
                else
                {
                    continue;
                }
            }
            return treeDataViews;
        }

       private List<TreeDataView> BuildChildTreeView(DataRowObject parentdataRowObject, Dictionary<string, List<DataRowObject>> dataObjectRows
            , string parentfieldName, string keyFieldName, string alternatekeyFieldName, List<TreeDataView> treeDataViewList, List<object> parentKeys)
        {
            var parentKeyValue = String.IsNullOrEmpty(alternatekeyFieldName) ? parentdataRowObject.Columns[keyFieldName].ToString() : parentdataRowObject.Columns[keyFieldName].ToString() + parentdataRowObject.Columns[alternatekeyFieldName].ToString();
            List<DataRowObject> childDataRowObjects;
            dataObjectRows.TryGetValue(parentKeyValue, out childDataRowObjects);
            // = dataObjectRows.FindAll(row => row.Columns.Count > 0 && row.Columns[parentfieldName].Equals(parentKeyValue));
            if (childDataRowObjects != null)
                foreach (DataRowObject childDataRowObject in childDataRowObjects)
                {
                    if (childDataRowObject.RowState == RowState.Deleted || childDataRowObject.Columns["IsProcessed"].Equals(true))
                        continue;

                    var keyValue = childDataRowObject.Columns[keyFieldName];
                    List<object> parentKeyList = new List<object>();
                    parentKeyList.AddRange(parentKeys);
                    parentKeyList.Add(keyValue);

                    childDataRowObject.Columns["primarykey"] = parentKeyList;
                    childDataRowObject.Columns["IsProcessed"] = true;
                    treeDataViewList.Add(new TreeDataView()
                    {
                        ParentKey = "primarykey",
                        ParentValue = parentKeyList,
                        Row = childDataRowObject,
                    });

                    // finding grand children, if no grandChildren then do not call BuildChildTreeView
                    // var isAnyGrandChildren = dataObjectRows.Find(grandChildRow => grandChildRow.Columns.Count > 0 && grandChildRow.Columns[parentfieldName].Equals(parentKeyValue)) != null;
                    // if (isAnyGrandChildren)
                    treeDataViewList = BuildChildTreeView(childDataRowObject, dataObjectRows
                        , parentfieldName, keyFieldName, alternatekeyFieldName, treeDataViewList, parentKeyList);
                }
            return treeDataViewList;
        }
       
    }

    
}