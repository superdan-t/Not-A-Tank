import networkstreams
import tankmanager

version = '0.0.0'

print('Welcome to TankServer v' + version + '!')

networkstreams.start_server()
tankmanager.begin_tank_checking()

hostname = networkstreams.socket_hostname
port = networkstreams.socket_port

sustain = True

while sustain:
    line_in = input('>>| ')
    line_segments = line_in.split()

    if len(line_segments) > 0:

        line_segments[0] = line_segments[0].lower()

        if line_segments[0] == 'quit' or line_segments[0] == 'exit' or line_segments[0] == 'stop':
            sustain = False
        elif line_segments[0] == 'help':
            print('=======[Help topics for TankServer]=======\n')
            print('activity    Display the number of active tanks. Use -l to list.')
            print('apply       Apply changes in hostname or port to the server')
            print('hostname    Change the hostname of the server. Otherwise, system default is used')
            print('port        Change the port of the server. Not recommended unless it is changed on the tank as well')
            print('stop        Exit the server program. Equivalent to both "quit" and "exit"')
            print('=======[            END           ]=======\n')

        elif line_segments[0] == 'activity':

            if len(line_segments) > 1 and line_segments[1] == '-l':
                print('=======[Active Tanks]=======')
                for tank in tankmanager.active_tanks:
                    print(tank.dump_details())
                print('=======[    END     ]=======')
            else:
                print('There are ' + str(len(tankmanager.active_tanks)) + ' active tanks.')

        elif line_segments[0] == 'apply':
            networkstreams.change_properties(hostname=hostname, port=port)

        elif line_segments[0] == 'hostname':
            hostname = line_segments[1]

        elif line_segments[0] == 'port':
            port = int(line_segments[1])

        else:
            print('Unknown command. Type "help" for a list of commands.')

