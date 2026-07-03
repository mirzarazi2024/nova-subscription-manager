"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-03
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('hiddify_user_id', sa.String(length=128), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hiddify_user_id')
    )
    op.create_index(op.f('ix_users_hiddify_user_id'), 'users', ['hiddify_user_id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)

    op.create_table(
        'providers',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('authentication', sa.JSON(), nullable=True),
        sa.Column('cache_duration_seconds', sa.Integer(), nullable=False),
        sa.Column('update_interval_seconds', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('last_update_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('health_score', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('scoring_speed', sa.Float(), nullable=False),
        sa.Column('scoring_healthy_nodes', sa.Float(), nullable=False),
        sa.Column('scoring_dead_ratio', sa.Float(), nullable=False),
        sa.Column('scoring_response_time', sa.Float(), nullable=False),
        sa.Column('scoring_error_rate', sa.Float(), nullable=False),
        sa.Column('scoring_total', sa.Float(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'countries',
        sa.Column('iso_code', sa.String(length=8), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('flag_emoji', sa.String(length=16), nullable=False),
        sa.Column('continent', sa.String(length=64), nullable=True),
        sa.Column('timezone', sa.String(length=64), nullable=True),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('iso_code')
    )

    op.create_table(
        'rules',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('condition', sa.JSON(), nullable=False),
        sa.Column('action', sa.JSON(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'api_keys',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=64), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key_hash'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'scheduler_jobs',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('cron', sa.String(length=64), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('next_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'settings',
        sa.Column('key', sa.String(length=255), nullable=False),
        sa.Column('value', sa.JSON(), nullable=False),
        sa.Column('encrypted', sa.Boolean(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )

    op.create_table(
        'backups',
        sa.Column('backup_type', sa.String(length=64), nullable=False),
        sa.Column('storage_url', sa.String(length=1024), nullable=False),
        sa.Column('checksum', sa.String(length=128), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'logs',
        sa.Column('level', sa.String(length=32), nullable=False),
        sa.Column('logger', sa.String(length=128), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('context', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logs_level'), 'logs', ['level'], unique=False)

    op.create_table(
        'audit_logs',
        sa.Column('actor', sa.String(length=255), nullable=False),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('target', sa.String(length=255), nullable=False),
        sa.Column('changes', sa.JSON(), nullable=False),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('actor', 'action', 'target', 'created_at', name='uq_audit_tuple')
    )
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_actor'), 'audit_logs', ['actor'], unique=False)
    op.create_index(op.f('ix_audit_logs_target'), 'audit_logs', ['target'], unique=False)

    op.create_table(
        'subscriptions',
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('uuid', sa.String(length=128), nullable=False),
        sa.Column('source_hiddify_url', sa.String(length=1024), nullable=True),
        sa.Column('nova_url', sa.String(length=1024), nullable=False),
        sa.Column('format', sa.String(length=32), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('preview_summary', sa.JSON(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nova_url'),
        sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=False)
    op.create_index(op.f('ix_subscriptions_uuid'), 'subscriptions', ['uuid'], unique=False)

    op.create_table(
        'provider_nodes',
        sa.Column('provider_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('protocol', sa.String(length=32), nullable=False),
        sa.Column('server', sa.String(length=255), nullable=False),
        sa.Column('port', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=255), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('tls', sa.Boolean(), nullable=False),
        sa.Column('reality', sa.Boolean(), nullable=False),
        sa.Column('transport', sa.String(length=64), nullable=True),
        sa.Column('sni', sa.String(length=255), nullable=True),
        sa.Column('country_code', sa.String(length=8), nullable=True),
        sa.Column('city', sa.String(length=128), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('health', sa.String(length=32), nullable=False),
        sa.Column('latency_ms', sa.Float(), nullable=False),
        sa.Column('fingerprint', sa.String(length=128), nullable=False),
        sa.Column('raw_payload', sa.JSON(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_nodes_fingerprint'), 'provider_nodes', ['fingerprint'], unique=False)
    op.create_index(op.f('ix_provider_nodes_protocol'), 'provider_nodes', ['protocol'], unique=False)
    op.create_index(op.f('ix_provider_nodes_provider_id'), 'provider_nodes', ['provider_id'], unique=False)
    op.create_index(op.f('ix_provider_nodes_server'), 'provider_nodes', ['server'], unique=False)

    op.create_table(
        'health_checks',
        sa.Column('node_fingerprint', sa.String(length=128), nullable=False),
        sa.Column('check_type', sa.String(length=32), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('latency_ms', sa.Float(), nullable=False),
        sa.Column('packet_loss', sa.Float(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_health_checks_node_fingerprint'), 'health_checks', ['node_fingerprint'], unique=False)

    op.create_table(
        'merged_nodes',
        sa.Column('subscription_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('provider_node_id', postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column('source', sa.String(length=32), nullable=False),
        sa.Column('node_name', sa.String(length=255), nullable=False),
        sa.Column('protocol', sa.String(length=32), nullable=False),
        sa.Column('fingerprint', sa.String(length=128), nullable=False),
        sa.Column('rank_score', sa.Float(), nullable=False),
        sa.Column('final_payload', sa.JSON(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['provider_node_id'], ['provider_nodes.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_merged_nodes_fingerprint'), 'merged_nodes', ['fingerprint'], unique=False)
    op.create_index(op.f('ix_merged_nodes_subscription_id'), 'merged_nodes', ['subscription_id'], unique=False)


def downgrade() -> None:
    op.drop_table('merged_nodes')
    op.drop_table('health_checks')
    op.drop_table('provider_nodes')
    op.drop_table('subscriptions')
    op.drop_index(op.f('ix_audit_logs_target'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_actor'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index(op.f('ix_logs_level'), table_name='logs')
    op.drop_table('logs')
    op.drop_table('backups')
    op.drop_table('settings')
    op.drop_table('scheduler_jobs')
    op.drop_table('api_keys')
    op.drop_table('rules')
    op.drop_table('countries')
    op.drop_table('providers')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_hiddify_user_id'), table_name='users')
    op.drop_table('users')
