using System;
using System.Collections.Generic;
using PerformanceConsoleApp.Models;

namespace PerformanceConsoleApp.Services
{
    public class TreeViewBuilder
    {
        public List<TreeDataView> BuildTreeView(DataTableObject dataTable, TreeView treeView)
        {
            List<TreeDataView> treeDataViews = new List<TreeDataView>();
            List<DataRowObject> dataRowObjects = dataTable.Rows.FindAll(x => x.Columns.Count > 0 && !x.Columns["IsProcessed"].Equals(true));
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
            foreach (DataRowObject dataRow in dataRowObjects)
            {
                if (dataRow.RowState == RowState.Deleted || dataRow.Columns["IsProcessed"].Equals(true))
                    continue;

                DataRowObject dataRowObject = dataRowObjects.Find(x => x.Columns.Count > 0 &&
                                            alternatekeyFieldName.Equals(String.Empty) ?
                                            x.Columns[keyFieldName].Equals(dataRow.Columns[parentfieldName]) :
                                            (x.Columns[keyFieldName].ToString() + x.Columns[alternatekeyFieldName].ToString()).Equals(dataRow.Columns[parentfieldName]));

                if (dataRowObject == null || (dataRowObject.Columns[parentfieldName].Equals(String.Empty) && dataRowObject.Columns[keyFieldName].Equals(String.Empty)) || dataRowObject.Columns[keyFieldName].Equals(dataRowObject.Columns[parentfieldName]))
                {
                    var attributeValue = dataRow.Columns[keyFieldName];
                    List<object> parentKeyList = new List<object>();
                    parentKeyList.Add(attributeValue);

                    treeDataViews.Add(new TreeDataView()
                    {
                        ParentKey = "primarykey",
                        ParentValue = parentKeyList,
                        Row = dataRow,
                    });

                    dataRow.Columns["primarykey"] = parentKeyList;
                    dataRow.Columns["IsProcessed"] = true;
                    treeDataViews = BuildChildTreeView(dataRow, dataTable, parentfieldName, keyFieldName, alternatekeyFieldName, treeDataViews, parentKeyList);
                }
                else
                {
                    continue;
                }
            }
            return treeDataViews;
        }

        private List<TreeDataView> BuildChildTreeView(DataRowObject dataRow, DataTableObject dataTable, string parentfieldName, string keyFieldName, string alternatekeyFieldName, List<TreeDataView> treeDataViewList, List<object> parentKeys)
        {

           List<DataRowObject> dataRowObjects = dataTable.Rows.FindAll(x => x.Columns.Count > 0 && !x.Columns["IsProcessed"].Equals(true) &&
                                                                       x.Columns[parentfieldName].Equals(alternatekeyFieldName.Equals(String.Empty)
                                                                       ? dataRow.Columns[keyFieldName] : dataRow.Columns[keyFieldName].ToString() + dataRow.Columns[alternatekeyFieldName].ToString()));

           foreach (DataRowObject dataRowObject in dataRowObjects)
           {
               if (dataRowObject.RowState == RowState.Deleted || dataRowObject.Columns["IsProcessed"].Equals(true))
                   continue;

               if (dataTable.Rows.Find(x => x.Columns.Count > 0 && x.Columns[parentfieldName].Equals(alternatekeyFieldName.Equals(String.Empty) ?
                                       dataRowObject.Columns[keyFieldName] : dataRowObject.Columns[keyFieldName].ToString() + dataRowObject.Columns[alternatekeyFieldName].ToString())) == null)
               {
                   var attributeValue = dataRowObject.Columns[keyFieldName];

                   List<object> parentKeyList = new List<object>();
                   foreach (var item in parentKeys)
                   {
                       parentKeyList.Add(item);
                   }
                   parentKeyList.Add(attributeValue);

                   dataRowObject.Columns["IsProcessed"] = true;
                   dataRowObject.Columns["primarykey"] = parentKeyList;
                   treeDataViewList.Add(new TreeDataView()
                   {
                       ParentKey = "primarykey",
                       ParentValue = parentKeyList,
                       Row = dataRowObject,
                   });
               }
               else
               {
                   var attributeValue = dataRowObject.Columns[keyFieldName];
                   List<object> parentKeyList = new List<object>();
                   foreach (var item in parentKeys)
                   {
                       parentKeyList.Add(item);
                   }
                   parentKeyList.Add(attributeValue);

                   treeDataViewList.Add(new TreeDataView()
                   {
                       ParentKey = "primarykey",
                       ParentValue = parentKeyList,
                       Row = dataRowObject,
                   });
                   dataRowObject.Columns["primarykey"] = parentKeyList;
                   dataRowObject.Columns["IsProcessed"] = true;
                   treeDataViewList = BuildChildTreeView(dataRowObject, dataTable, parentfieldName, keyFieldName, alternatekeyFieldName, treeDataViewList, parentKeyList);
               }
           }
           return treeDataViewList;
       }
    }
}
