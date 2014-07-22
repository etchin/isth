// This Processing sketch shows chart plots on each location and allows to construct a cluster of selected locations.
// A new column indicating whether each patient belongs to the cluster or not is added to the data and saved to disk
// when pressing a key.

import de.fhpotsdam.unfolding.*;
import de.fhpotsdam.unfolding.marker.*;
import de.fhpotsdam.unfolding.geo.*;
import de.fhpotsdam.unfolding.utils.*;
import java.util.HashSet;

UnfoldingMap map;
Table data, dict, locs;
ArrayList<String> locIds;
HashMap<String, String> locNames;
HashMap<String, Location> locLatLon;
HashMap<String, Integer> locDeaths;
HashMap<String, Integer> locTotals;
int maxTotal;

Location locationISTH = new Location(6.731770, 6.190593);
PShape star;

PFont font;

void setup() {
  size(800, 800, P2D);
  noStroke();
  
  font = createFont("Courier", 12);
  
  loadData();
  initLocations();
  calculateCFR();
  
  map = new UnfoldingMap(this);
  map.setTweening(true);
  map.zoomAndPanTo(7, locationISTH);
  MapUtils.createDefaultEventDispatcher(this, map);
  
  initStar();
  initMarkers();
}

void draw() {  
  background(0);
  map.draw();
  
  ScreenPosition posISTH = map.getScreenPosition(locationISTH);
  shape(star, posISTH.x, posISTH.y);
} 

void mouseMoved() {
  for (Marker marker : map.getMarkers()) {
    marker.setSelected(false);
  }

  // Select hit marker
  // Note: Use getHitMarkers(x, y) if you want to allow multiple selection.
  Marker marker = map.getFirstHitMarker(mouseX, mouseY);
  if (marker != null) {
    marker.setSelected(true);
  }
}

void mouseReleased() {
  CFRMarker marker = (CFRMarker)map.getFirstHitMarker(mouseX, mouseY);
  if (marker != null) {
    if (marker.insideCluster()) {
      marker.removeFromCluster();
    } else {
      marker.addToCluster();
    }
  }
}

void keyPressed() {
  HashSet<String> clust = new HashSet<String>();  
  for (Marker marker : map.getMarkers()) {
    CFRMarker cfrm = (CFRMarker)marker;
    if (cfrm.insideCluster()) {
      println(cfrm.id + " " +locNames.get(cfrm.id));
      clust.add(cfrm.id);
    } 
  }
  
  int locIdx = data.getColumnIndex("Place of residence");
  int outIdx = data.getColumnIndex("Outcome");
  String[] lines = new String[data.getRowCount()]; 
  for (int i = 0; i < data.getRowCount(); i++) {
    TableRow row = data.getRow(i);
    String loc = row.getString(locIdx);
    String out = row.getString(outIdx);
    if (clust.contains(loc)) {
      lines[i] = "1";
//      println("patient " + i + " is inside the cluster " + out);
//      println("1");
    } else {
      lines[i] = "2";
    }    
  }
  saveStrings("cluster.txt", lines);
  
} 

void loadData() {
  data = loadTable("data.tsv", "header");
  dict = loadTable("dictionary.tsv");   
  data.setMissingString("\\N");
  data.setColumnTypes(dict); 
}

void initLocations() {
  locIds = new ArrayList<String>();
  locNames = new HashMap<String, String>();
  locLatLon = new HashMap<String, Location>();
  locTotals = new HashMap<String, Integer>();
  locDeaths = new HashMap<String, Integer>();

  TableRow locRow = dict.getRow(4);
  String nameString = locRow.getString(2);
  String[] idNames = nameString.split(";");
  for (String idn: idNames) {
    String[] parts = idn.split(":");
    String id = parts[0];
    String name = parts[1];
    locIds.add(id);
    locNames.put(id, name);
    locTotals.put(id, 0);
    locDeaths.put(id, 0);
  }

  Table locs = loadTable("locations.tsv");
  locs.setColumnType(0, Table.STRING);
  locs.setColumnType(1, Table.FLOAT);
  locs.setColumnType(2, Table.FLOAT);
  for (int i = 0; i < locs.getRowCount(); i++) {
    TableRow row = locs.getRow(i);
    String id = row.getString(0);
    float lat = row.getFloat(1);
    float lon = row.getFloat(2); 
    Location loc = new Location(lat, lon);
    locLatLon.put(id, loc);   
  }
}

void calculateCFR() {
  int locIdx = data.getColumnIndex("Place of residence");
  int outIdx = data.getColumnIndex("Outcome");
  for (int i = 0; i < data.getRowCount(); i++) {
    TableRow row = data.getRow(i);
    String loc = row.getString(locIdx);
    String out = row.getString(outIdx);
    
    if (!loc.equals("\\N")) {
      locTotals.put(loc, locTotals.get(loc) + 1);
      if (out.equals("2")) {
        locDeaths.put(loc, locDeaths.get(loc) + 1);      
      }
    }
  }
  
  maxTotal = 0;
  for (String loc: locTotals.keySet()) {
    maxTotal = max(maxTotal, locTotals.get(loc));
  }  
  println(maxTotal);
}

void initStar() {
  star = createShape();
  star.beginShape();
  star.fill(102, 150);
  star.noStroke();
  star.strokeWeight(2);
  star.vertex(0, -50);
  star.vertex(14, -20);
  star.vertex(47, -15);
  star.vertex(23, 7);
  star.vertex(29, 40);
  star.vertex(0, 25);
  star.vertex(-29, 40);
  star.vertex(-23, 7);
  star.vertex(-47, -15);
  star.vertex(-14, -20);
  star.endShape(CLOSE);  
  star.scale(0.5);
}

void initMarkers() {
  for (String id: locIds) {
    ScreenPosition pos = map.getScreenPosition(locLatLon.get(id));
    CFRMarker marker = new CFRMarker(id, locLatLon.get(id), locNames.get(id), locTotals.get(id), locDeaths.get(id), maxTotal, font);
    map.addMarkers(marker);    
  }  
}
