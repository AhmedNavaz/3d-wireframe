import math
import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

vertices = []
faces = []
edges = []


def read_file():
    with open("object.txt", "r") as file:
        # Read the first line
        line = file.readline()
        num_vertices, num_faces = [int(x) for x in line.split(",")]

        # Read the vertices
        for i in range(num_vertices):
            line = file.readline()
            vertex = [float(x) for x in line.split(",")[1:]]
            vertices.append(vertex)

        # make each vertex multiple of 100
        for i in range(len(vertices)):
            vertices[i] = [x * 100 for x in vertices[i]]

        # Read the faces
        for i in range(num_faces):
            line = file.readline()
            face = [int(x) for x in line.split(",")]
            faces.append(face)

        # create a list of edges from the faces which are 1-6  but use 0-5
        for face in faces:
            for i in range(len(face)):
                edges.append((face[i] - 1, face[(i + 1) % len(face)] - 1))

    print(vertices)
    print(faces)
    print(edges)


# rotate the tetrahedron
def rotate(angle, axis):
    # rotation matrix
    if axis == "x":
        rotation_matrix = [[1, 0, 0], [0, math.cos(angle), -math.sin(angle)], [0, math.sin(angle), math.cos(angle)]]
    elif axis == "y":
        rotation_matrix = [[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]]
    else:
        rotation_matrix = [[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0], [0, 0, 1]]

    # rotate the vertices
    for i in range(len(vertices)):
        vertices[i] = [sum(a * b for a, b in zip(rotation_matrix[j], vertices[i])) for j in range(len(rotation_matrix))]

    return vertices


# draw colored faces
def draw_faces():
    for face in faces:
        # calculate the normal of the face as there are 6 vertices and 8 faces
        normal = [0, 0, 0]
        for i in range(len(face)):
            normal[0] += (vertices[face[i] - 1][1] - vertices[face[(i + 1) % len(face)] - 1][1]) * (
                    vertices[face[i] - 1][2] + vertices[face[(i + 1) % len(face)] - 1][2])
            normal[1] += (vertices[face[i] - 1][2] - vertices[face[(i + 1) % len(face)] - 1][2]) * (
                    vertices[face[i] - 1][0] + vertices[face[(i + 1) % len(face)] - 1][0])
            normal[2] += (vertices[face[i] - 1][0] - vertices[face[(i + 1) % len(face)] - 1][0]) * (
                    vertices[face[i] - 1][1] + vertices[face[(i + 1) % len(face)] - 1][1])

        # calculate the angle between the normal and the z axis
        angle = math.acos(normal[2] / math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2))

        # calculate the color
        color = (0, 0, int(95 + 160 * angle / math.pi))

        # draw the face
        pygame.draw.polygon(screen, color, [(int(vertices[face[i] - 1][0] + width / 2), int(vertices[
                                                                                                face[i] - 1][
                                                                                                1] + height / 2))
                                            for i in range(len(face))])


def main():
    # Read the object file
    global vertices
    read_file()
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # rotate the object with the mouse movement
            if event.type == pygame.MOUSEMOTION:
                x, y = event.rel
                vertices = rotate(-x / 100, "y")
                vertices = rotate(y / 100, "x")

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the edges of the tetrahedron
        for edge in edges:
            pygame.draw.line(screen, (0, 0, 255),
                             (int(vertices[edge[0]][0] + width / 2), int(vertices[edge[0]][1] + height / 2)),
                             (int(vertices[edge[1]][0] + width / 2), int(vertices[edge[1]][1] + height / 2)), 2)

        # draw the vertices of the tetrahedron
        for vertex in vertices:
            pygame.draw.circle(screen, (0, 0, 255), (int(vertex[0] + width / 2), int(vertex[1] + height / 2)), 5)

        # draw the faces of the tetrahedron
        draw_faces()

        # Update the display
        pygame.display.update()


if __name__ == "__main__":
    main()
