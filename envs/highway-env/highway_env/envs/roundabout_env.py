from __future__ import division, print_function, absolute_import
from gym.envs.registration import register
import numpy as np

from highway_env import utils
from highway_env.envs.common.abstract import AbstractEnv
from highway_env.road.lane import LineType, StraightLane, CircularLane, SineLane
from highway_env.road.road import Road, RoadNetwork
from highway_env.vehicle.control import MDPVehicle


class RoundaboutEnv(AbstractEnv):

    COLLISION_REWARD = -1
    HIGH_VELOCITY_REWARD = 0.2
    RIGHT_LANE_REWARD = 0
    LANE_CHANGE_REWARD = -0.05

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            "incoming_vehicle_destination": None,
            "screen_width": 600,
            "screen_height": 600,
            "centering_position": [0.5, 0.6],
            "duration": 11
        })
        return config

    def _reward(self, action):
        reward = self.COLLISION_REWARD * self.vehicle.crashed \
                 + self.HIGH_VELOCITY_REWARD * self.vehicle.velocity_index / max(self.vehicle.SPEED_COUNT - 1, 1)
        if not self.config["low_level"]:
            reward += self.LANE_CHANGE_REWARD * (action in [0, 2])
        return utils.remap(reward, [self.COLLISION_REWARD+self.LANE_CHANGE_REWARD, self.HIGH_VELOCITY_REWARD], [0, 1])

    def _is_terminal(self):
        """
            The episode is over when a collision occurs or when the access ramp has been passed.
        """
        return self.vehicle.crashed or self.steps >= self.config["duration"]

    def reset(self):
        self._make_road()
        self._make_vehicles()
        self.steps = 0
        return super(RoundaboutEnv, self).reset()

    def step(self, action):
        self.steps += 1
        return super(RoundaboutEnv, self).step(action)

    def _make_road(self):
        # Circle lanes: (s)outh/(e)ast/(n)orth/(w)est (e)ntry/e(x)it.
        center = [0, 0]  # [m]
        radius = 30  # [m]
        alpha = 20  # [deg]

        net = RoadNetwork()
        radii = [radius, radius+4]
        n, c, s = LineType.NONE, LineType.CONTINUOUS, LineType.STRIPED
        line = [[c, s], [n, c]]
        for lane in [0, 1]:
            net.add_lane("se", "ex", CircularLane(center, radii[lane], rad(90-alpha), rad(alpha), clockwise=False, line_types=line[lane]))
            net.add_lane("ex", "ee", CircularLane(center, radii[lane], rad(alpha), rad(-alpha), clockwise=False, line_types=line[lane]))
            net.add_lane("ee", "nx", CircularLane(center, radii[lane], rad(-alpha), rad(-90+alpha), clockwise=False, line_types=line[lane]))
            net.add_lane("nx", "ne", CircularLane(center, radii[lane], rad(-90+alpha), rad(-90-alpha), clockwise=False, line_types=line[lane]))
            net.add_lane("ne", "wx", CircularLane(center, radii[lane], rad(-90-alpha), rad(-180+alpha), clockwise=False, line_types=line[lane]))
            net.add_lane("wx", "we", CircularLane(center, radii[lane], rad(-180+alpha), rad(-180-alpha), clockwise=False, line_types=line[lane]))
            net.add_lane("we", "sx", CircularLane(center, radii[lane], rad(180-alpha), rad(90+alpha), clockwise=False, line_types=line[lane]))
            net.add_lane("sx", "se", CircularLane(center, radii[lane], rad(90+alpha), rad(90-alpha), clockwise=False, line_types=line[lane]))

        # Access lanes: (r)oad/(s)ine
        access = 200  # [m]
        dev = 120  # [m]
        a = 5  # [m]
        delta_st = 0.20*dev  # [m]

        delta_en = dev-delta_st
        w = 2*np.pi/dev
        net.add_lane("ser", "ses", StraightLane([2, access], [2, dev/2], line_types=[s, c]))
        net.add_lane("ses", "se", SineLane([2+a, dev/2], [2+a, dev/2-delta_st], a, w, -np.pi/2, line_types=[c, c]))
        net.add_lane("sx", "sxs", SineLane([-2-a, -dev/2+delta_en], [-2-a, dev/2], a, w, -np.pi/2+w*delta_en, line_types=[c, c]))
        net.add_lane("sxs", "sxr", StraightLane([-2, dev / 2], [-2, access], line_types=[n, c]))

        net.add_lane("eer", "ees", StraightLane([access, -2], [dev / 2, -2], line_types=[s, c]))
        net.add_lane("ees", "ee", SineLane([dev / 2, -2-a], [dev / 2 - delta_st, -2-a], a, w, -np.pi / 2, line_types=[c, c]))
        net.add_lane("ex", "exs", SineLane([-dev / 2 + delta_en, 2+a], [dev / 2, 2+a], a, w, -np.pi / 2 + w * delta_en, line_types=[c, c]))
        net.add_lane("exs", "exr", StraightLane([dev / 2, 2], [access, 2], line_types=[n, c]))

        net.add_lane("ner", "nes", StraightLane([-2, -access], [-2, -dev / 2], line_types=[s, c]))
        net.add_lane("nes", "ne", SineLane([-2 - a, -dev / 2], [-2 - a, -dev / 2 + delta_st], a, w, -np.pi / 2, line_types=[c, c]))
        net.add_lane("nx", "nxs", SineLane([2 + a, dev / 2 - delta_en], [2 + a, -dev / 2], a, w, -np.pi / 2 + w * delta_en, line_types=[c, c]))
        net.add_lane("nxs", "nxr", StraightLane([2, -dev / 2], [2, -access], line_types=[n, c]))

        road = Road(network=net, np_random=self.np_random, record_history=self.config["show_trajectories"])
        self.road = road

    def _make_vehicles(self):
        """
            Populate a road with several vehicles on the highway and on the merging lane, as well as an ego-vehicle.
        :return: the ego-vehicle
        """
        position_deviation = 2
        velocity_deviation = 2

        # Ego-vehicle
        ego_lane = self.road.network.get_lane(("ser", "ses", 0))
        ego_vehicle = MDPVehicle(self.road,
                                 ego_lane.position(140, 0),
                                 velocity=5,
                                 heading=ego_lane.heading_at(140))\
            .plan_route_to(self.config["ego_vehicle_destination"]) # "nxs"
        MDPVehicle.SPEED_MIN = 0
        MDPVehicle.SPEED_MAX = 15
        MDPVehicle.SPEED_COUNT = 4
        self.road.vehicles.append(ego_vehicle)
        self.vehicle = ego_vehicle


        destinations = ["exr", "sxr", "nxr"]
        other_vehicles_type = utils.class_from_path(self.config["other_vehicles_type"])

        # Incoming vehicle

        for i in range(self.config["num_incoming_vehicle"]):
            vehicle = other_vehicles_type.make_on_lane(self.road,
                                                       ("we", "sx", 1),
                                                       longitudinal=5+ 10*i + self.np_random.randn()*position_deviation,
                                                       velocity=16 + self.np_random.randn()*velocity_deviation)

            if self.config["incoming_vehicle_destination"] is not None:
                destination = destinations[self.config["incoming_vehicle_destination"]]
            else:
                destination = self.np_random.choice(destinations)
            vehicle.plan_route_to(destination)
            vehicle.randomize_behavior()
            self.road.vehicles.append(vehicle)

        # Other vehicles

        for i in list(range(1, int(self.config["num_other_vehicle"]/2) + 1)) \
                 + list(range(-int(self.config["num_other_vehicle"]/2), 0)):
            vehicle = other_vehicles_type.make_on_lane(self.road,
                                                       ("we", "sx", 0),
                                                       longitudinal=20*i + self.np_random.randn()*position_deviation,
                                                       velocity=16 + self.np_random.randn()*velocity_deviation)
            if self.config["other_vehicle_destination"] is not None:
                destination = destinations[self.config["other_vehicle_destination"]]
            else:
                destination = self.np_random.choice(destinations)
            vehicle.plan_route_to(destination)
            vehicle.randomize_behavior()
            self.road.vehicles.append(vehicle)

        # Entering vehicle

        for i in range(self.config["num_entering_vehicle"]):
            vehicle = other_vehicles_type.make_on_lane(self.road,
                                                       ("eer", "ees", 0),
                                                       longitudinal=100 + 50*i + self.np_random.randn() * position_deviation,
                                                       velocity=16 + self.np_random.randn() * velocity_deviation)
            destination = "exr"
            vehicle.plan_route_to(destination)
            # vehicle.plan_route_to(self.np_random.choice(destinations))
            vehicle.randomize_behavior()
            self.road.vehicles.append(vehicle)

        for i in range(self.config["num_entering_vehicle"]):
            vehicle = other_vehicles_type.make_on_lane(self.road,
                                                       ("ner", "nes", 0),
                                                       longitudinal=100 + 50*i + self.np_random.randn() * position_deviation,
                                                       velocity=16 + self.np_random.randn() * velocity_deviation)
            destination = "nxr"
            vehicle.plan_route_to(destination)
            # vehicle.plan_route_to(self.np_random.choice(destinations))
            vehicle.randomize_behavior()
            self.road.vehicles.append(vehicle)


def rad(deg):
    return deg*np.pi/180


class RoundaboutEnv_v1(RoundaboutEnv):

    # observation types:
    # Kinematics: num_observed_vehicles(6) x FeatureSize(5)
    # OccupancyGrid: FeatureSize(3) x GridSize(11) x GridSize(11)
    # GrayscaleObservation: ObsShape(84) x ObsShape(84) x StackSize(4), remember to change "screen_width" and "height"
    # TimeToCollision: state 3x3x10 , 3 lane 3 vehicle 10 horizon
    # KinematicsGoal: may not be needed and may need change

    # behavior type: IDMVehicle, LinearVehicle, AggressiveVehicle, DefensiveVehicle

    def change_config(self, config):
        self.config = config

    @classmethod
    def default_config(cls):
        """
            Default environment configuration.

            Can be overloaded in environment implementations, or by calling configure().
        :return: a configuration dict
        """
        config = {
            "observation": {
                "type": "Kinematics",
                # following parameters used in "GrayscaleObservation"
                "weights": [0.2989, 0.5870, 0.1140],  # weights for RGB conversion,
                "stack_size": 4,
                "observation_shape": (84, 84)
            },
            "policy_frequency": 15,  # [Hz]
            "other_vehicles_type": "highway_env.vehicle.behavior.IDMVehicle",
            "ego_vehicle_destination": "sxs",
            "incoming_vehicle_destination": 2,  # None, possible exit ["exr", "sxr", "nxr"]
            "other_vehicle_destination": 0,  # None, possible exit ["exr", "sxr", "nxr"]
            "entering_vehicle_destination": 2,  # None, possible exit ["exr", "sxr", "nxr"]
            "screen_width": 600, # all scene: 600, local image shape default: 84
            "screen_height": 600, #
            "centering_position": [0.5, 0.5],
            "duration": 200,
            "show_trajectories": False,
            "num_incoming_vehicle": 0,
            "num_other_vehicle": 0,
            "num_entering_vehicle": 0,
            "range": 30, # perception radius (m)
            "low_level": False # low level control for ego vehicle
        }
        return config


register(
    id='roundabout-v1',
    entry_point='highway_env.envs:RoundaboutEnv_v1',
)

register(
    id='roundabout-v0',
    entry_point='highway_env.envs:RoundaboutEnv',
)
