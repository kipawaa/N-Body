using System;

class Planet {
	public int[] position = new int[2];
	public int[] velocity = new int[2];
	public int mass;
	private double radius;
	
	public Planet(int x, int y, int xvel, int yvel, int planetMass) {
		position[0] = x;
		position[1] = y;
		velocity[0] = xvel;
		velocity[1] = yvel;
		mass = planetMass;
		radius = Math.Pow(mass / Math.PI, 1/3);
	}

	public void move(int dx, int dy) {
		position[0] += dx;
		position[1] += dy;
	}

	public void calcVelocity(Planet[] planets) {
		for (int i = 0; i < planets.Length; i++) {
			//TODO this is incomplete.
		}
	}

}

class Simulation {
	static void Main() {
		Planet earth = new Planet(0, 0, 0, 0, 1000);
		Console.WriteLine(earth.mass);
	}
}
