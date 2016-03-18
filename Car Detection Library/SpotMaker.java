import java.awt.Image;
import java.awt.image.BufferedImage;
public class SpotMaker {
	SpotDetector[] cutSpot;
	BufferedImage readyForSpot;
	SpotMaker(BufferedImage readyForSpot){
		this.readyForSpot = readyForSpot;
	}
	private SpotDetector SpotCutter(BufferedImage readyForSaving,int height, int width, int startX, int startY, boolean is_busy){
		BufferedImage ret = new BufferedImage(width, height,Image.SCALE_FAST);

		for(int x = startX; x < width + startX;x++){
			for(int y = startY; y < height + startY;y++){
				ret.setRGB(x - startX,y - startY,readyForSaving.getRGB(x, y));
				System.out.println(y);
			}
		}
		return new SpotDetector(ret, is_busy);

	}
	public SpotDetector[] cutSpots(int[] startX,int[] startY,int[] endX,int[] endY,boolean[] is_busy){
		SpotDetector[] ret = new SpotDetector[startX.length];
		for (int x = 0; x < startX.length; x++) {
				ret[x] = SpotCutter(this.readyForSpot,  endY[x] - startY[x], endX[x] - startX[x],startX[x], startY[x], is_busy[x]);
			}
		this.cutSpot = ret;
		return ret;
	}

}
