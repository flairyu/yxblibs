package yxb.tool;

import java.awt.BorderLayout;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;

import java.awt.FlowLayout;

import javax.swing.ButtonGroup;
import javax.swing.JFileChooser;
import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.JRadioButton;
import javax.swing.JTextArea;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.io.File;
import javax.swing.JLabel;

public class Main extends JFrame implements Loger{

	private JPanel contentPane;
	private JTextField filepath;
	private JTextArea log;
	private JButton button_start;
	private JTextField fileExt;
	
	public static int logcount[] = new int[3];
	public final static int LOG = 0;
	public final static int WARNING = 1;
	public final static int ERROR = 2;
	private FileChangeAlpha fca;
	private int linenum = 1;
	
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Main frame = new Main();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public Main() {
		
		fca = new FileChangeAlpha(FileChangeAlpha.TransMode.UpperToLower, this);
		
		setTitle("Alpha Transformer ---- Redice®");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 611, 407);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(new BorderLayout(0, 0));
		
		JPanel panel = new JPanel();
		contentPane.add(panel, BorderLayout.NORTH);
		panel.setLayout(new FlowLayout(FlowLayout.LEFT, 5, 5));
		
		filepath = new JTextField();
		filepath.setToolTipText("File Path");
		panel.add(filepath);
		filepath.setColumns(15);
		
		JButton btnbrowsing = new JButton("Browsing...");
		btnbrowsing.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				Log("Browsing for file path..");
				JFileChooser jf = new JFileChooser("Chose files or directory to process..");
				jf.setMultiSelectionEnabled(true);
				jf.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
				if (fileExt.getText().trim().isEmpty() == false ) {
					FileNameExtensionFilter filter = new FileNameExtensionFilter(
					        fileExt.getText(), fileExt.getText().split(","));
					jf.setFileFilter(filter);
				}
				int result = jf.showOpenDialog(Main.this);
				File[] selectedFile = null;
				if (result == JFileChooser.APPROVE_OPTION) {
				    System.out.println("OK button is pushed.");
				    selectedFile = jf.getSelectedFiles();
				    String filepaths = "";
				    for(File f:selectedFile) {
				    	filepaths += f.getPath() + ",";
				    	Log("you chose:" + f.getPath());
				    }
				    filepath.setText(filepaths);
				} else if (result == JFileChooser.CANCEL_OPTION) {
				    Log("Canceled.");
				} else if (result == JFileChooser.ERROR_OPTION) {
				    Log("Error when select file.");
				}
			}
		});
		
		fileExt = new JTextField();
		fileExt.setToolTipText("file extension name");
		fileExt.setText("txt,");
		panel.add(fileExt);
		fileExt.setColumns(3);
		panel.add(btnbrowsing);
		
		ButtonGroup group = new ButtonGroup(); 
		
		JRadioButton rdbtnAa = new JRadioButton("A->a");
		rdbtnAa.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Log("Change to Upper to Lower mode.");
				fca.SetMode(FileChangeAlpha.TransMode.UpperToLower);
			}
		});
		rdbtnAa.setSelected(true);
		group.add(rdbtnAa);
		panel.add(rdbtnAa);
		
		JRadioButton rdbtnaA = new JRadioButton("a->A");
		rdbtnaA.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Log("Change to Lower to Upper mode.");
				fca.SetMode(FileChangeAlpha.TransMode.LowerToUpper);
			}
		});
		group.add(rdbtnaA);
		panel.add(rdbtnaA);
		
		button_start = new JButton("Start");
		button_start.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				if (button_start.getText() == "Start") {
				
					Log("Start to process..");
					logcount[0] = logcount[1] = logcount[2] = 0;
					if (filepath.getText().trim().isEmpty()) {
						Error("please chose files first!");
						return;
					}
					
					button_start.setText("Stop");
					new Thread() {
						public void run() {
							int count = fca.TransFiles(filepath.getText(), fileExt.getText());
							button_start.setText("Start");
							Log("Done.");
							Log("-------------------------------");
							Log("Process Files:" + count);
							Log("Warnnings:" + logcount[WARNING]);
							Log("Errors:" + logcount[ERROR]);
						}
					}.start();
					
				} else {
					Log("User stop the process.");
					button_start.setText("Start");
					fca.Stop();
				}
			}
		});
		panel.add(button_start);
		
		JPanel panel_1 = new JPanel();
		contentPane.add(panel_1, BorderLayout.CENTER);
		panel_1.setLayout(new BorderLayout(0, 0));
		
		log = new JTextArea();
		panel_1.add(log, BorderLayout.CENTER);
		
	}

	public void Error(String msg) {
		showLog(ERROR, msg);
	}
	
	public void Warnning(String msg) {
		showLog(WARNING, msg);
	}
	
	public void Log(String msg) {
		showLog(LOG, msg);
	}
	
	private void showLog(int level, String msg) {
		assert(level>=0 && level<3);
		String strs[] = {">Log:",">War:",">Err:"};
		String str = log.getText();
		str = linenum + strs[level]+msg+"\r\n"+str;
		logcount[level]++;
		linenum++;
		log.setText(str);
	}
	
}
