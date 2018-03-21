#!/usr/bin/python3
"""
    Visual aid to track personal fitness
"""
import blinkt
import time
import boto3

def get_steps(client):
    """
        Return the steps logged
    """
    num_steps = 0

    try:
        response = client.invoke(
            FunctionName='fitbit-pi0-get-steps'
        )

    except Exception as error:
        print(error)
    else:
        str_steps = str(response['Payload'].read(), 'utf-8').strip('"')
        try:
            num_steps = int(str_steps)
        except ValueError:
            return -1
    return num_steps


if __name__ == "__main__":
    client = boto3.client('lambda')

    blinkt.set_brightness(0.1)
    current_time = time.time()

    # retrieve steps
    steps = get_steps(client)
    print(str(steps))
    denominator = int(10000 / 8)
    num_leds = steps // denominator

    while True:
        # update steps every 15 minutes
        if (time.time() - current_time) > 900:
            steps = get_steps(client)
            print("In loop" + str(steps))
            # refresh LEDs only if step check was successful
            if steps >= 0:
                current_time = time.time()
                num_leds = steps // denominator
            else:
                continue

            for i in range(8):
                blinkt.set_pixel(i, 0, 0, 0)
                blinkt.set_brightness(0.1)
                blinkt.show()

        if num_leds > 8:
            num_leds = 8

        for i in range(num_leds):
            blinkt.set_pixel(i, 0, 255, 0)
            blinkt.set_brightness(0.1)
            blinkt.show()

        if num_leds <= 7:
            blinkt.set_pixel(num_leds, 255, 0, 0)
            blinkt.set_brightness(0.1)
            blinkt.show()
            time.sleep(1)
            blinkt.set_pixel(num_leds, 0, 0, 0)
            blinkt.set_brightness(0.1)
            blinkt.show()
            time.sleep(1)
