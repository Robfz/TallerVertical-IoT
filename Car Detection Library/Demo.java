import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JFileChooser;

public class Demo {

	public static void main(String[] args) {
		JFileChooser a = new JFileChooser();
		a.showOpenDialog(null);
		SpotDetector b = null;
		while(b == null){
			try {
				b = new SpotDetector(ImageIO.read(a.getSelectedFile()), false);
			} catch (IOException e) {
				System.out.println("Mean image exception try again.");
			}
		}
		while(true){
			try {
				a.showOpenDialog(null);
				b.setSpot(ImageIO.read(a.getSelectedFile()));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				System.out.println("Mean image exception try again.");
			}
		}
	}


}
