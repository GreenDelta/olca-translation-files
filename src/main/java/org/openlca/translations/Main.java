package org.openlca.translations;

import java.io.File;
import java.util.List;

public class Main {

	static void main() {

		var inbox = new File("inbox");
		var files = inbox.listFiles();
		if (files == null) {
			System.out.println("No files in inbox");
			return;
		}

		for (var f : files) {
			var target = findTarget(f.getName());
			if (target == null) {
				System.out.println("Was removed: " + f.getName());
				continue;
			}

			try {
				var inProps = Props.read(f);
				var props = Props.read(target);
				props.putAll(inProps);
				var out = new File("outbox/" + target.getName());
				Props.write(props, out);
			} catch (Exception e) {
				System.out.println(f.getName() + " :: "  + e.getMessage());
			}
		}
	}

	private static File findTarget(String name) {
		var dirs = List.of("app-messages", "bundle-messages");
		for (var d : dirs) {
			var dir = new File(d);
			var files = dir.listFiles();
			if (files == null)
				continue;
			for (var f : files) {
				if (f.getName().equalsIgnoreCase(name))
					return f;
			}
		}
		return null;
	}
}
