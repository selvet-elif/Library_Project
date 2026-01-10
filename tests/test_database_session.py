"""Tests for database session management."""
import pytest
from unittest.mock import AsyncMock, patch
from app.database import get_session


@pytest.mark.asyncio
async def test_get_session_generator():
    """Test get_session is an async generator."""
    import inspect
    
    # Verify it's an async generator
    assert inspect.isasyncgenfunction(get_session)
    
    # Test that it yields a session (mocked)
    with patch("app.database.async_session_maker") as mock_session_maker:
        mock_session = AsyncMock()
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_session)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_session_maker.return_value = mock_context
        
        # Get the generator
        gen = get_session()
        
        # Get the session
        session = await gen.__anext__()
        
        # Verify session was created
        assert session == mock_session
        
        # Clean up
        try:
            await gen.__anext__()  # Should raise StopAsyncIteration
        except StopAsyncIteration:
            pass  # Expected
