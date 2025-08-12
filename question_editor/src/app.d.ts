declare global {
  namespace App {}
}

declare module "simple-datatables" {
  export { DataTable } from "simple-datatables/dist/dts/datatable";
  export { convertCSV, convertJSON } from "simple-datatables/dist/dts/convert";
  export { exportCSV, exportJSON, exportSQL, exportTXT } from "simple-datatables/dist/dts/export";
  export { createElement, isJson, isObject } from "simple-datatables/dist/dts/helpers";
  export { makeEditable } from "simple-datatables/dist/dts/editing";
  export { addColumnFilter } from "simple-datatables/dist/dts/column_filter";

  export type {
    DataTableOptions,
    DataTableConfiguration,
    ColumnOption,
    cellType,
    inputCellType,
    dataRowType,
    inputRowType,
    headerCellType,
    inputHeaderCellType,
    TableDataType,
    DataOption,
    renderType,
    nodeType,
    elementNodeType,
    textNodeType,
    cellDataType
  } from "simple-datatables/dist/dts/datatable";

  export interface SelectableDataRow {
    selected?: boolean;
    [key: string]: any;
  }
}

declare global {
	interface Window {
		api?: {
			getBackendPort?: () => number;
			// add other exposed methods here
		};
	}
}

export {};
