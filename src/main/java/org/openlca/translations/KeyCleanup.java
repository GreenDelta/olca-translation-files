package org.openlca.translations;

import java.io.File;
import java.nio.file.Files;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Pattern;

/// This file removes unused keys from the `app-messages/messages*.properties`
/// files. It first reads the translation keys from the `src/M.java` file. That
/// file is copied from openLCA. Before running the cleanup, make sure that this
/// is the current version of the file from openLCA. It then removes all
/// translations from the app-messages, for which the key is not defined in
/// `M.java`.
public class KeyCleanup {

	private final Set<String> keys;

	private KeyCleanup(Set<String> keys) {
		this.keys = keys;
	}

	static void main() {
		var mFile = new File("src/M.java");
		if (!mFile.exists()) {
			System.out.println("No M.java file found at: " + mFile);
			return;
		}
		try {
			var keys = readKeys(mFile);
			System.out.println("Found " + keys.size()
				+ " keys in " + mFile.getName());
			new KeyCleanup(keys).run();
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	private void run() {
		var dir = new File("app-messages");
		var files = dir.listFiles(f -> f.isFile()
			&& f.getName().startsWith("messages")
			&& f.getName().endsWith(".properties"));
		if (files == null) {
			System.out.println("No message files found");
			return;
		}
		for (var file : files) {
			clean(file);
		}
	}

	private void clean(File file) {
		var props = Props.read(file);
		var removed = new TreeSet<String>();
		for (var key : props.stringPropertyNames()) {
			if (keys.contains(key))
				continue;
			props.remove(key);
			removed.add(key);
		}
		if (removed.isEmpty()) {
			System.out.println("No unused keys in " + file.getName());
			return;
		}
		Props.write(props, file);
		System.out.println("Removed " + removed.size()
			+ " keys from " + file.getName());
		for (var key : removed) {
			System.out.println("  " + key);
		}
	}

	private static Set<String> readKeys(File file) throws Exception {
		var pattern = Pattern.compile(
			"public\\s+static\\s+String\\s+(\\w+)\\s*;");
		var keys = new TreeSet<String>();
		for (var line : Files.readAllLines(file.toPath())) {
			var m = pattern.matcher(line);
			if (m.find()) {
				keys.add(m.group(1));
			}
		}
		return keys;
	}
}
