class CFRMarker extends SimplePointMarker {
  String id;
  String name;
  int totCount;
  int deathCount;
  float radius;
  PFont font;
  boolean inside;

  CFRMarker(Location location) {
    this.location = location;
  }

  CFRMarker(String id, Location location, String name, int tot, int death, int maxtot, PFont font) {
    this(location);
    this.id = id;
    this.name = name;
    this.totCount = tot;
    this.deathCount = death;
    this.font = font;
    
    
    radius = map(sqrt(totCount / PI), 0, sqrt(maxtot / PI), 5, 50);
    inside = false;
  }

  void draw(PGraphics pg, float x, float y) {
    pg.pushStyle();
    pg.pushMatrix();
//    if (selected) {
//      pg.translate(0, 0, 1);
//    }


/*
    pg.strokeWeight(strokeWeight);
    if (selected) {
      pg.fill(100, 0, 0, 180);
      pg.stroke(highlightStrokeColor);
    } else {
      pg.fill(255, 0, 0, 180);
      pg.stroke(strokeColor);
    }
    pg.ellipse(x, y, radius, radius);// TODO use radius in km and convert to px
*/


    pg.noStroke();
    float dangle = TAU * (float)deathCount / totCount;
    pg.fill(255, 0, 0, 150);    
    pg.arc((int)x, (int)y, radius, radius, 0, dangle, PApplet.PIE);
    pg.fill(0, 0, 255, 150);
    pg.arc((int)x, (int)y, radius, radius, dangle, TAU, PApplet.PIE);
    if (inside) {
      pg.stroke(0);
      pg.noFill();
      pg.ellipse(x, y, radius, radius);
    }



    // label
//    if (selected && name != null) {
//      if (font != null) {
//        pg.textFont(font);
//      }
//      pg.fill(highlightColor);
//      pg.stroke(highlightStrokeColor);
//      pg.rect(x + strokeWeight / 2, y - fontSize + strokeWeight / 2 - space, pg.textWidth(name) + space * 1.5f,
//          fontSize + space);
//      pg.fill(255, 255, 255);
//      pg.text(name, Math.round(x + space * 0.75f + strokeWeight / 2),
//          Math.round(y + strokeWeight / 2 - space * 0.75f));
//    }

    pg.popMatrix();
    pg.popStyle();
  }

  String getName() {
    return name;
  }
  
  void addToCluster() {
    inside = true;
  }
  
  void removeFromCluster() {
    inside = false;
  }

  boolean insideCluster() {
    return inside;
  }  
}
