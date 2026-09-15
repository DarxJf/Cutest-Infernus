from typing import Any, Optional

from gale.ai import BehaviorTree, Selector, Sequence, Condition, Action, Status

import settings
from src.Utils.MovementCalculator import MovementCalculator


def build_enemy_brain() -> BehaviorTree:
    # --- aux funcs ---
    def get_target(agent: Any) -> Optional[Any]:
        # MAnhattan
        alive = [ally for ally in agent.party if not getattr(ally, 'dead', False)]
        if not alive: 
            return None
        return min(
            alive, 
            key=lambda a: abs(a.mapX - agent.currentActor.mapX) + abs(a.mapY - agent.currentActor.mapY)
        )

    def get_valid_attack(agent: Any, target: Any) -> Optional[Any]:
        if not target: 
            return None
            
        dist = abs(target.mapX - agent.currentActor.mapX) + abs(target.mapY - agent.currentActor.mapY)

        available_actions = []
        if agent.currentActor.basicAttack:
            available_actions.append(agent.currentActor.basicAttack)
            
        for act in agent.currentActor.actionSlots:
            if act.name not in agent.currentActor.skillCooldowns:
                available_actions.append(act)

        for act in available_actions:
            if dist <= act.gridRange:
                return act
        return None
    
    # --- Questions ---
    def can_attack(agent) -> bool:
        target = get_target(agent)
        return get_valid_attack(agent, target) is not None

    def can_move(agent) -> bool:
        return not getattr(agent, 'hasMoved', False)

    # --- Actions ---
    def do_attack(agent, dt) -> Status:
        target = get_target(agent)
        attack = get_valid_attack(agent, target)

        agent.resolve_action(agent.currentActor, attack, target.mapX, target.mapY, is_enemy=True)

        return Status.SUCCESS

    def do_move(agent, dt) -> Status:
        actor = agent.currentActor
        target = get_target(agent)
        
        if not target:
            return Status.FAILURE

        available_tiles = MovementCalculator.get_available_moves(
            actor.mapX, actor.mapY, actor.baseMovement, agent.room.is_walkable
        )

        occupied = {(e.mapX, e.mapY) for e in agent.party + agent.enemies if not getattr(e, 'dead', False)}

        path = MovementCalculator.get_path_to_target(
            actor.mapX, actor.mapY, target.mapX, target.mapY, agent.room.is_walkable
        )
        
        best_tile = None

        if path and len(path) > 1:
            if path[0] == (actor.mapX, actor.mapY):
                path.pop(0)
                
            for step in path:
                if step in available_tiles:
                    if step != (target.mapX, target.mapY) and step not in occupied:
                        best_tile = step
                else:
                    break

        if not best_tile:
            return Status.FAILURE

        actor.mapX, actor.mapY = best_tile
        actor.x = best_tile[0] * settings.TILE_SIZE
        actor.y = best_tile[1] * settings.TILE_SIZE

        agent.hasMoved = True

        return Status.SUCCESS

    def pass_turn(agent, dt) -> Status:
        agent.turnQueue.end_turn(agent.currentActor, action_cost_multiplier=1.0)
        agent.start_next_turn()

        return Status.SUCCESS

    tree = BehaviorTree(
        Selector([
            Sequence([Condition(can_attack), Action(do_attack)]),
            Sequence([Condition(can_move), Action(do_move)]),
            Action(pass_turn)
        ])
    )
    
    return tree
