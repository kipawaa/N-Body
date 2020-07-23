/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package nbody;

import java.util.ArrayList;
import java.util.Random;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.Stroke;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.geom.Ellipse2D;
import javax.swing.JApplet;
import javax.swing.JFrame;

/**
 *
 * @author River
 */
public class NBody extends JApplet {
    
    private static final int NUM_PLANETS = 100;
    private ArrayList<Planet> planets;
    
    private double G = 6.67408*(Math.pow(10, -11));
    
    public NBody() {
        Random x = new Random();
        for (int i = 0; i < NUM_PLANETS; i ++) {
            
            double xpos = x.nextDouble();
            double ypos = x.nextDouble();
            double xvel = x.nextDouble();
            double yvel = x.nextDouble();
            double radius;
            int mass;
            mass = x.nextInt(900);
            mass += 100;
            
            radius = Math.sqrt(mass/Math.PI);
            Planet planet = new Planet(xpos, ypos, xvel, yvel, mass, radius);
            planets.add(planet);
        }
    }
    
    //advance method
    public void advance() {
        double[] xvelocities = new double[planets.size()];
        double[] yvelocities = new double[planets.size()];
        
        for (int i = 0; i < planets.size(); i ++) {
            double totalForce;
            
            for (int j = 0; j < planets.size(); j ++) {
                Planet a = planets.get(i);
                Planet b = planets.get(j);
                
                double xmagnitude = a.x()-b.x();
                double ymagnitude = a.y()-b.y();
                
                double xforce = G*a.mass()*b.mass()*xmagnitude;
                double yforce = G*a.mass()*b.mass()*ymagnitude;
                
                double xaccel = xforce/a.mass();
                double yaccel = yforce/a.mass();
                
                xvelocities[i] += xaccel;
                yvelocities[i] += yaccel;
                
            }
        }
        
        for (int i = 0; i < planets.size(); i ++) {
            Planet a = planets.get(i);
            
            //move each planet
            a.moveX(xvelocities[i]);
            a.moveY(yvelocities[i]);
            
            for (int j = 0; j < planets.size(); j ++) {
                Planet b = planets.get(j);
                
                //calculate distances
                double xdist = a.x()-b.x();
                double ydist = a.x()-b.x();
                double dist = Math.sqrt(Math.pow(xdist, 2) + Math.pow(ydist, 2));
                
                //detect collisions
                if (dist < a.radius()+b.radius()) {
                    //collisions
                    
                    //create new planet
                    Planet planet = new Planet(a.x()+b.x()/2, a.y()+b.y()/2, a.xVelocity()+b.xVelocity(), a.yVelocity()+b.yVelocity(), a.mass()+b.mass(), Math.sqrt(((a.mass()+b.mass()))/Math.PI));
                    planets.add(planet);
                    
                    //remove old planets
                    planets.remove(a);
                    planets.remove(b);
                }
                
            }
        }
        
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
    } // end of main
    
}
