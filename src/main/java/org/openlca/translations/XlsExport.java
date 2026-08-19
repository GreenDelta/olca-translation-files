package org.openlca.translations;

import java.io.File;
import java.io.FileOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;
import java.util.TreeSet;

import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class XlsExport {

	private final String lang;

	private XlsExport(String lang) {
		this.lang = lang;
	}

	public static void write(String lang) {
		new XlsExport(lang).run();
	}

	private void run() {
		var appMessages = appMessages();
		if (appMessages == null)
			return;
		var bundleMessages = bundleMessages();
		if (bundleMessages == null)
			return;

		try (var wb = new XSSFWorkbook()) {
			var appSheet = wb.createSheet("app-messages");
			appMessages.writeTo(appSheet);
			var bundleSheet = wb.createSheet("bundle-messages");
			bundleMessages.writeTo(bundleSheet);
			Files.createDirectories(Path.of("outbox"));
			var file = new File("outbox/olca-translations_" + lang + ".xlsx");
			try (var stream = new FileOutputStream(file)) {
				wb.write(stream);
			}
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	private Trans appMessages() {
		var enFile = new File("app-messages/messages.properties");
		if (!enFile.exists()) {
			System.out.println("English translation is missing");
			return null;
		}
		var english = Props.read(enFile);
		if (lang.equals("en"))
			return new Trans(lang, english, english);

		var langFile = new File("app-messages/messages_" + lang + ".properties");
		if (!langFile.exists()) {
			System.out.println("No messages found for language: " + lang);
			return null;
		}

		var translated = Props.read(langFile);
		return new Trans(lang, english, translated);
	}

	private Trans bundleMessages() {
		var enFile = new File("bundle-messages/bundle.properties");
		if (!enFile.exists()) {
			System.out.println("English bundle translation is missing");
			return null;
		}
		var english = Props.read(enFile);
		if (lang.equals("en"))
			return new Trans(lang, english, english);

		var langFile = new File("bundle-messages/bundle_" + lang + ".properties");
		if (!langFile.exists())
			return new Trans(lang, english, new Properties());

		var translated = Props.read(langFile);
		return new Trans(lang, english, translated);
	}

	private record Trans(
		String lang, Properties english, Properties translated
	) {

		void writeTo(Sheet sheet) {
			int i = 0;
			var keys = new TreeSet<>(english.stringPropertyNames());
			for (var key : keys) {
				var row = sheet.createRow(i++);
				row.createCell(1).setCellValue("#" + key);
				row = sheet.createRow(i++);
				row.createCell(1).setCellValue(english.getProperty(key));
				row = sheet.createRow(i++);
				row.createCell(0).setCellValue(lang);
				row.createCell(1).setCellValue(translated.getProperty(key, ""));
				i++;
			}
			sheet.autoSizeColumn(0);
			sheet.setColumnWidth(1, 100 * 256);
		}

	}

	static void main() {

		var files = new File("app-messages").listFiles();
		if (files == null) {
			System.out.println("No translation files found");
			return;
		}

		var codes = new TreeSet<String>();
		codes.add("en");
		for (var f : files) {
			var pos = f.getName().indexOf('_');
			if (pos < 0)
				continue;
			var code = f.getName()
				.substring(pos + 1)
				.replace(".properties", "");
			codes.add(code);
		}

		for (var code : codes) {
			System.out.println("Export language: " + code);
			XlsExport.write(code);
		}


	}
}
