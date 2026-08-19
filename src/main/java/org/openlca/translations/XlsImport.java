package org.openlca.translations;

import java.io.File;
import java.io.FileInputStream;
import java.util.Properties;

import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class XlsImport {

	private final String lang;
	private final File file;

	private XlsImport(String lang, File file) {
		this.lang = lang;
		this.file = file;
	}

	public static void read(String lang) {
		var file = new File("inbox/olca-translations_" + lang + ".xlsx");
		read(file);
	}

	public static void read(File file) {
		var lang = langOf(file);
		if (lang == null) {
			System.out.println("Could not determine language of file "
				+ file.getName());
			return;
		}
		System.out.println("Import " + file.getName() + " (language " + lang + ")");
		new XlsImport(lang, file).run();
	}

	private void run() {
		if (!file.exists()) {
			System.out.println("No file found: " + file.getName());
			return;
		}
		try (var wb = new XSSFWorkbook(new FileInputStream(file))) {
			importSheet(wb.getSheet("app-messages"),
				"app-messages/messages");
			importSheet(wb.getSheet("bundle-messages"),
				"bundle-messages/bundle");
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	private void importSheet(Sheet sheet, String base) {
		if (sheet == null) {
			System.out.println("Sheet is missing for: " + base);
			return;
		}
		var propsFile = lang.equals("en")
			? new File(base + ".properties")
			: new File(base + "_" + lang + ".properties");
		var props = propsFile.exists()
			? Props.read(propsFile)
			: new Properties();
		var changed = false;
		for (int i = 0; i <= sheet.getLastRowNum(); i += 4) {
			var key = keyOf(sheet.getRow(i));
			if (key == null)
				continue;
			var value = valueOf(sheet.getRow(i + 2));
			if (value == null || value.isEmpty())
				continue;
			props.setProperty(key, value);
			changed = true;
		}
		if (changed) {
			Props.write(props, propsFile);
			System.out.println("Updated " + propsFile.getName());
		}
	}

	private static String keyOf(Row row) {
		if (row == null)
			return null;
		var cell = row.getCell(1);
		if (cell == null)
			return null;
		var key = cell.getStringCellValue();
		if (key == null || key.isEmpty())
			return null;
		return key.startsWith("#")
			? key.substring(1)
			: key;
	}

	private static String valueOf(Row row) {
		if (row == null)
			return null;
		var cell = row.getCell(1);
		return cell == null
			? null
			: cell.getStringCellValue();
	}

	private static String langOf(File file) {
		var name = file.getName();
		var prefix = "olca-translations_";
		if (!name.startsWith(prefix) || !name.endsWith(".xlsx"))
			return null;
		return name.substring(
			prefix.length(), name.length() - ".xlsx".length());
	}

	static void main() {
		var inbox = new File("inbox");
		var files = inbox.listFiles(f -> f.isFile()
			&& f.getName().endsWith(".xlsx"));
		if (files == null) {
			System.out.println("No files in inbox");
			return;
		}
		for (var f : files) {
			read(f);
		}
	}
}