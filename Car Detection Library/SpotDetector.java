import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;

public class SpotDetector {


	private int height;
	private int width;

	private int averageR = 0;
	private int averageG = 0;
	private int averageB = 0;

	private int averageRB = 0;
	private int averageGB = 0;
	private int averageBB = 0;

	private boolean is_busy;

	private BufferedImage spot;


	SpotDetector(BufferedImage spot, boolean is_busy){
		this.height = spot.getHeight();
		this.width = spot.getWidth();
		this.is_busy = is_busy;
		this.spot = spot;
		this.compress();
		this.getAverage();
	}
	public void compress(){
		BufferedImage original = this.spot;
		int newWidth = new Double(original.getWidth() * .05).intValue();
		int newHeight = new Double(original.getHeight() * .05).intValue();
		BufferedImage resized = new BufferedImage(newWidth, newHeight, original.getType());
		Graphics2D g = resized.createGraphics();
		g.setRenderingHint(RenderingHints.KEY_INTERPOLATION,
		    RenderingHints.VALUE_INTERPOLATION_BILINEAR);
		g.drawImage(original, 0, 0, newWidth, newHeight, 0, 0, original.getWidth(),
		    original.getHeight(), null);
		g.dispose();
	}

	private void getAverage(){
		this.backup();
		for(int x = 0; x < this.width;x++){
			for(int y = 0; y < this.height;y++){
				Color c = new Color(this.spot.getRGB(x, y));
				this.averageR += c.getRed();
				this.averageG += c.getGreen();
				this.averageB += c.getBlue();
			}
			this.averageR /= this.height;
			this.averageG /= this.height;
			this.averageB /= this.height;
		}
	}


	private void backup(){
		this.averageRB = this.averageR;
		this.averageGB = this.averageG;
		this.averageBB = this.averageB;

		System.out.println(this.averageRB);
		System.out.println(this.averageGB);
		System.out.println(this.averageBB);
		
		this.averageR = 0;
		this.averageG = 0;
		this.averageB = 0;
	}


	private boolean hasChanged(){
		this.getAverage();
		if(Math.abs(this.averageBB - this.averageB)> 10 && Math.abs(this.averageGB - this.averageG)> 10 && Math.abs(this.averageRB - this.averageR)> 10){
			this.is_busy = !this.is_busy;
			if(this.is_busy){
				System.out.println("Someone has arrived.");
			}else{
				System.out.println("A spot has been freed :)");
			}
			return true;
		}else{
			System.out.println("Nothing has changed.");
			return false;
		}
	}
	
	
	public void setSpot(BufferedImage newSpot){
		this.spot = newSpot;
		this.hasChanged();
		
	}
}

