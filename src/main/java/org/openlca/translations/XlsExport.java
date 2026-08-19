package org.openlca.translations;

import java.io.File;
import java.io.FileOutputStream;
import java.util.Properties;
import java.util.TreeSet;

import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class XlsExport {

	/**
	 * Writes the translations of the given language to an Excel file. The file
	 * has two sheets (messages and bundles) where each entry is written in the
	 * following format: the key (prefixed with a hash), the English text, the
	 * translation, and an empty row.
	 */
	public static void write(String lang) {
		try (var workbook = new XSSFWorkbook()) {
			writeSheet(workbook.createSheet("messages"),
				"app-messages", "messages", lang);
			writeSheet(workbook.createSheet("bundles"),
				"bundle-messages", "bundle", lang);
			var file = new File("outbox/olca-translations_" + lang + ".xlsx");
			try (var stream = new FileOutputStream(file)) {
				workbook.write(stream);
			}
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	private static void writeSheet(Sheet sheet, String dir,
		String base, String lang) {
		var defaults = Props.read(new File(dir, base + ".properties"));
		var translatedFile = new File(dir, base + "_" + lang + ".properties");
		var translated = translatedFile.exists()
			? Props.read(translatedFile)
			: new Properties();
		int rowIndex = 0;
		var keys = new TreeSet<>(defaults.stringPropertyNames());
		for (var key : keys) {
			var row = sheet.createRow(rowIndex++);
			row.createCell(1).setCellValue("#" + key);
			row = sheet.createRow(rowIndex++);
			row.createCell(1).setCellValue(defaults.getProperty(key));
			row = sheet.createRow(rowIndex++);
			row.createCell(0).setCellValue(lang);
			row.createCell(1).setCellValue(translated.getProperty(key, ""));
			rowIndex++;
		}
		sheet.autoSizeColumn(0);
		sheet.setColumnWidth(1, 100 * 256);
	}

	static void main() {
		XlsExport.write("ar");
	}
}
