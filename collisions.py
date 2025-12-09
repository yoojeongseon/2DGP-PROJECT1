# (파일: collisions.py)

import pygame
from visual_effects import VisualEffect


def handle_player_collisions(player1, player2, effect_group, effect_frames, sounds):
    """
    타격 판정, 이펙트 생성, 사운드 재생 (펀치 소리는 항상 재생)
    """

    AWAKEN_MULTIPLIER = 1.5

    # ==================================================
    # 1. P1 공격 -> P2 피격 판정
    # ==================================================
    absolute_hitbox_p1 = player1.get_absolute_hitbox()

    if (absolute_hitbox_p1 and
            player1.has_hit == False and
            player2.is_alive):

        if absolute_hitbox_p1.colliderect(player2.hurtbox_absolute):
            player1.has_hit = True

            # 1. [공통] 펀치 소리는 무조건 재생! (막혀도 소리 남)
            attack_type = player1.current_state
            if attack_type in sounds:
                sounds[attack_type].play()

            # 이펙트 위치 계산
            hit_pos = (
                (absolute_hitbox_p1.centerx + player2.hurtbox_absolute.centerx) // 2,
                (absolute_hitbox_p1.centery + player2.hurtbox_absolute.centery) // 2
            )

            # 2. 상태별 분기
            if player2.current_state == 'Blocking':
                print("P2 Blocked!")
                # [이펙트] 방어 이펙트
                if 'BlockEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['BlockEffect'])
                    effect_group.add(effect)

                # [사운드] 방어 소리 추가 재생 (펀치음 + 방어음)
                if 'Block' in sounds:
                    sounds['Block'].play()

            elif player2.current_state == 'Dizzy':
                print("P2 is Invincible!")

            else:
                # [타격 성공]
                if 'HitEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['HitEffect'])
                    effect_group.add(effect)

                # 데미지 처리
                was_alive = player2.is_alive

                current_attack = player1.attacks[player1.current_state]
                if current_attack.is_ko_move:
                    player2.take_damage(player2.max_hp)
                else:
                    damage = current_attack.damage
                    if player1.is_awakened: damage *= AWAKEN_MULTIPLIER
                    player2.take_damage(damage)

                # KO 종소리
                if was_alive and not player2.is_alive:
                    if 'Bell' in sounds: sounds['Bell'].play()

    # ==================================================
    # 2. P2 공격 -> P1 피격 판정
    # ==================================================
    absolute_hitbox_p2 = player2.get_absolute_hitbox()

    if (absolute_hitbox_p2 and
            player2.has_hit == False and
            player1.is_alive):

        if absolute_hitbox_p2.colliderect(player1.hurtbox_absolute):
            player2.has_hit = True

            # 1. [공통] 펀치 소리 재생
            attack_type = player2.current_state
            if attack_type in sounds:
                sounds[attack_type].play()

            hit_pos = (
                (absolute_hitbox_p2.centerx + player1.hurtbox_absolute.centerx) // 2,
                (absolute_hitbox_p2.centery + player1.hurtbox_absolute.centery) // 2
            )

            if player1.current_state == 'Blocking':
                print("P1 Blocked!")
                if 'BlockEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['BlockEffect'])
                    effect_group.add(effect)

                # [사운드] 방어 소리 추가 재생
                if 'Block' in sounds:
                    sounds['Block'].play()

            elif player1.current_state == 'Dizzy':
                print("P1 is Invincible!")

            else:
                # [타격 성공]
                if 'HitEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['HitEffect'])
                    effect_group.add(effect)

                # 데미지 처리
                was_alive = player1.is_alive

                current_attack = player2.attacks[player2.current_state]
                if current_attack.is_ko_move:
                    player1.take_damage(player1.max_hp)
                else:
                    damage = current_attack.damage
                    if player2.is_awakened: damage *= AWAKEN_MULTIPLIER
                    player1.take_damage(damage)

                # KO 종소리
                if was_alive and not player1.is_alive:
                    if 'Bell' in sounds: sounds['Bell'].play()