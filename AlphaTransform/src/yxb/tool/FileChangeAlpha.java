package yxb.tool;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.ArrayList;

public class FileChangeAlpha {
	
	private TransMode _mode = TransMode.UpperToLower;
	private Loger _log;
	private int _processed = 0;
	private boolean _isRunning = false;
	private String _filters[] = null; 
	public FileChangeAlpha(TransMode mode, Loger log) {
		assert(mode!=null && log!=null);
		_mode = mode;
		_log = log;
	}
	
	public enum TransMode {
		UpperToLower,
		LowerToUpper
	}
	
	public int TransFiles(String filepaths, String filter) {
		_processed = 0;
		_isRunning = true;
		if (filter.trim().isEmpty() == false ) {
			_filters = filter.split(",");
		} else {
			_filters = null;
		}
		String[] files = filepaths.split(",");
		for(String f:files) {
			if (f.isEmpty() == false && _isRunning) {
				Transfer(f);
			}
		}
		_isRunning = false;
		return _processed;
	}
	
	public int Stop() {
		_isRunning = false;
		return _processed;
	}
	
	public void SetMode(TransMode mode) {
		_mode = mode;
	}
	
	private void Transfer(String filepath) {
		if(!_isRunning) return;
		
		File file = new File(filepath);
		assert(file!=null);
		if (file.isDirectory()) {
			_log.Log("enter directory: "+file.getPath());
			File[] files = file.listFiles();
			for(File f:files) {
				Transfer(f.getPath());
			}
		} else if(file.isFile() && acceptFile(file.getName())) {
			_log.Log("processing: "+file.getPath());
			
			// read all
			ArrayList<String> contents = readAll(file);
			
			// don't concern empty file.
			if (contents.size() == 0) return;
			
			// trans alpha
			for(int i=0; i<contents.size(); i++) {
				String s = contents.get(i);
				if (_mode == TransMode.LowerToUpper) {
					s = s.toUpperCase();
				} else {
					s = s.toLowerCase();
				}
				contents.set(i, s);
			}
			
			// write all
			writeAll(contents, file);
			
			_processed++;
		}
	}
	
	private ArrayList<String> readAll(File file) {
		BufferedReader reader = null;
		ArrayList<String> contents = new ArrayList<String>();
		// read all
		try {
			
			FileReader fin = new FileReader(file);
			reader = new BufferedReader(fin);
			String str;
			while ( (str = reader.readLine()) != null ) {
				contents.add(str);
			}
			reader.close();
			reader = null;
			
		} catch (FileNotFoundException e) {
			_log.Warnning("file not found:" + file.getPath());
		} catch (IOException e) {
			_log.Warnning("file cannot read:" + file.getPath());
		} finally {
			if (reader!=null) {
				try {
					reader.close();
				} catch (IOException e) {
					_log.Warnning("file cannot close:" + file.getPath());
				}
			}
		}
		return contents;
	}
	
	private void writeAll(ArrayList<String> contents, File file) {
		BufferedWriter writer = null;
		// write all
		try {
			
			FileWriter fin = new FileWriter(file);
			writer = new BufferedWriter(fin);
			for(String s:contents) {
				writer.write(s);
				writer.newLine();
			}
			writer.close();
			writer = null;
			
		} catch (FileNotFoundException e) {
			_log.Warnning("file not found:" + file.getPath());
		} catch (IOException e) {
			_log.Warnning("file cannot write:" + file.getPath());
		} finally {
			if (writer!=null) {
				try {
					writer.close();
				} catch (IOException e) {
					_log.Warnning("file cannot close:" + file.getPath());
				}
			}
		}
	}
	
	private boolean acceptFile(String name) {
		if (_filters == null) return true;
		for (String s:_filters) {
			if (name.endsWith("."+s) ) return true;
		}
		return false;
	}
}
