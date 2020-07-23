/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package nbody;

/**
 *
 * @author River
 */
public class Planet {
    
    private double x;
    private double y;
    private double xVelocity;
    private double yVelocity;
    private double mass;
    private double radius;
    
    public Planet(double x, double y, double xVelocity, double yVelocity, double mass, double radius) {
        this.x = x;
        this.y = y;
        this.xVelocity = xVelocity;
        this.yVelocity = yVelocity;
        this.mass = mass;
        this.radius = radius;
    }
    
    public double x() {
        return x;
    }
    
    public double y() {
        return y;
    }
    
    public double xVelocity() {
        return xVelocity;
    }
    
    public double yVelocity() {
        return yVelocity;
    }
    
    public double mass() {
        return mass;
    }
    
    public double radius() {
        return radius;
    }
    
    public void setx(double x) {
        
    }
    
    public void sety() {
        
    }
    
    public void setxVel() {
        
    }
    
    public void setyVel() {
        
    }
    
    public void setMass() {
        
    }
    
    public void setRadius(double radius) {
        
    }
    
    public void moveX(double x) {
        this.x += x;
    }
    
    public void moveY(double y) {
        this.y += y;
    }
    
}
