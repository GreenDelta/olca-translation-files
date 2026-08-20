package org.openlca.translations;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import java.util.Enumeration;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Set;
import java.util.TreeSet;

class Props {

	static Properties read(File file) {
		try (var stream = new FileInputStream(file)) {
			var props = new Properties();
			props.load(stream);
			return props;
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}

	static void write(Properties props, File file) {
		var sorted = SortedProps.of(props);
		try (var stream = new FileOutputStream(file)) {
			sorted.store(stream, null);
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}

	private static class SortedProps extends Properties {

		static SortedProps of(Properties props) {
			var sorted = new SortedProps();
			sorted.putAll(props);
			return sorted;
		}

		@Override
		public Enumeration<Object> keys() {
			var sorted = new TreeSet<>(
				(a, b) -> a.toString().compareToIgnoreCase(b.toString())
			);
			sorted.addAll(keySet());
			return Collections.enumeration(sorted);
		}

		@Override
		public Set<Entry<Object, Object>> entrySet() {
			Set<Map.Entry<Object, Object>> sorted = new TreeSet<>(
				Comparator.comparing(
					e -> e.getKey().toString(), String.CASE_INSENSITIVE_ORDER)
			);
			sorted.addAll(super.entrySet());
			return sorted;
		}
	}
}
